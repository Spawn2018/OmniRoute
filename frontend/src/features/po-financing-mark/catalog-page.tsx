import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchPoFinancingMarks,
  type PoFinancingMarkRow,
} from "@/lib/po-financing-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PoFinancingMarkSave } from "./mark-form"

const helper = createColumnHelper<PoFinancingMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("financing_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function PoFinancingMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchPoFinancingMarks,
    queryKey: ["po-financing-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-po-financing-mark="board">
      <CatalogHeading
        title="Finansowanie zamówienia"
        subtitle="BR5.1 po_financing_mark · katalog HITL · nie FK purchase_order · nie wycena zapasu"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PoFinancingMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            financing_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj stance PO Financing…"
          tableKey={BUSINESS_LISTS.poFinancingMark.tableKey}
        />
      ) : null}
    </section>
  )
}
