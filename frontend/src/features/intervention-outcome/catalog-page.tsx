import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchInterventionOutcomes,
  type InterventionOutcomeRow,
} from "@/lib/intervention-outcomes-api"
import { getTenantContext } from "@/lib/tenant"
import { InterventionOutcomeSave } from "./mark-form"

const helper = createColumnHelper<InterventionOutcomeRow>()

const COLUMNS = [
  helper.accessor("outcome_code", { header: "Kod" }),
  helper.accessor("result_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function InterventionOutcomeDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchInterventionOutcomes,
    queryKey: ["intervention-outcomes", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-intervention-outcome="board">
      <CatalogHeading
        title="Wynik interwencji"
        subtitle="CI7 intervention_outcome · katalog HITL · nie SQL saved · nie marża"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <InterventionOutcomeSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            outcome_code: "Kod",
            result_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj wyniku interwencji…"
          tableKey={BUSINESS_LISTS.interventionOutcome.tableKey}
        />
      ) : null}
    </section>
  )
}
