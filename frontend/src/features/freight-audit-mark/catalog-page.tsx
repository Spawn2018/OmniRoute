import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchFreightAuditMarks,
  type FreightAuditMarkRow,
} from "@/lib/freight-audit-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FreightAuditMarkSave } from "./freight-audit-mark-form"

const helper = createColumnHelper<FreightAuditMarkRow>()
const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("audit_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function FreightAuditMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchFreightAuditMarks,
    queryKey: ["freight-audit-marks", orgId],
    retry: false,
  })
  return (
    <section className="flex flex-col gap-5" data-freight-audit-mark="board">
      <CatalogHeading
        title="Audyt frachtu"
        subtitle="CT10 freight_audit_mark · katalog HITL · nie druga marża"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <FreightAuditMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            audit_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj audytu…"
          tableKey={BUSINESS_LISTS.freightAuditMark.tableKey}
        />
      ) : null}
    </section>
  )
}
