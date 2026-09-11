import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchSlaClauses, type SlaClauseRow } from "@/lib/sla-clauses-api"
import { getTenantContext } from "@/lib/tenant"
import { SlaClauseSave } from "./sla-clause-form"

const helper = createColumnHelper<SlaClauseRow>()

const COLUMNS = [
  helper.accessor("clause_code", { header: "Kod" }),
  helper.accessor("metric_kind", { header: "Metryka" }),
  helper.accessor("threshold_label", { header: "Próg" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function SlaClauseDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchSlaClauses,
    queryKey: ["sla-clauses", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-sla-clause="board">
      <CatalogHeading
        title="Klauzula SLA"
        subtitle="CI1 sla_clause · katalog HITL · nie extract · nie kara SQL"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SlaClauseSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            clause_code: "Kod",
            metric_kind: "Metryka",
            threshold_label: "Próg",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj klauzul…"
          tableKey={BUSINESS_LISTS.slaClause.tableKey}
        />
      ) : null}
    </section>
  )
}
