import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchImpactScenarios, type ImpactScenarioRow } from "@/lib/impact-scenarios-api"
import { getTenantContext } from "@/lib/tenant"
import { ImpactScenarioSave } from "./scenario-form"

const helper = createColumnHelper<ImpactScenarioRow>()

const COLUMNS = [
  helper.accessor("scenario_code", { header: "Kod" }),
  helper.accessor("chain_label", { header: "Łańcuch" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function ImpactScenarioDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchImpactScenarios,
    queryKey: ["impact-scenarios", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-impact-scenario="board">
      <CatalogHeading
        title="Scenariusz skutku"
        subtitle="CI6 impact_scenario · katalog HITL · nie EBITDA SQL · nie wieża"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ImpactScenarioSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            scenario_code: "Kod",
            chain_label: "Łańcuch",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj scenariuszy…"
          tableKey={BUSINESS_LISTS.impactScenario.tableKey}
        />
      ) : null}
    </section>
  )
}
