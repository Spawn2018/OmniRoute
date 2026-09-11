import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchLegalHoldMarks, type LegalHoldMarkRow } from "@/lib/legal-hold-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LegalHoldMarkSave } from "./mark-form"

const helper = createColumnHelper<LegalHoldMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("hold_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function LegalHoldMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchLegalHoldMarks,
    queryKey: ["legal-hold-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-legal-hold-mark="board">
      <CatalogHeading
        title="Znacznik legal hold"
        subtitle="G8 legal_hold_mark · katalog HITL · nie eIDAS crypto · nie wipe"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <LegalHoldMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            hold_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika legal hold…"
          tableKey={BUSINESS_LISTS.legalHoldMark.tableKey}
        />
      ) : null}
    </section>
  )
}
