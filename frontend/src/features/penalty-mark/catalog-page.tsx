import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchPenaltyMarks, type PenaltyMarkRow } from "@/lib/penalty-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PenaltyMarkSave } from "./mark-form"

const helper = createColumnHelper<PenaltyMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("breach_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function PenaltyMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchPenaltyMarks,
    queryKey: ["penalty-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-penalty-mark="board">
      <CatalogHeading
        title="Znacznik kary"
        subtitle="CI5 penalty_mark · katalog HITL · nie kara SQL · nie marża"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PenaltyMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            breach_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika kary…"
          tableKey={BUSINESS_LISTS.penaltyMark.tableKey}
        />
      ) : null}
    </section>
  )
}
