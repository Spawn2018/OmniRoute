import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadCounterfactualRuns,
  type CounterfactualRunRow,
} from "@/lib/counterfactual-runs-api"
import { getTenantContext } from "@/lib/tenant"
import { CounterfactualRunComposer } from "./ledger-form"

const helper = createColumnHelper<CounterfactualRunRow>()
const COLS = [
  helper.accessor("run_code", { header: "Kod" }),
  helper.accessor("baseline_label", { header: "Punkt" }),
  helper.accessor("levers_label", { header: "Dźwignie" }),
  helper.accessor("result_label", { header: "Wynik" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function CounterfactualRunBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadCounterfactualRuns,
    queryKey: ["counterfactual-runs", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div
      className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]"
      data-counterfactual-run="desk"
    >
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Przebieg what-if"
          subtitle="AI1.2 · run_code + etykiety · bez silnika"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL zapis nazwanego przebiegu — tylko dane.</li>
          <li>Punkt odniesienia, dźwignie i wynik jako tekst. Bez kwoty.</li>
          <li>Silnik what-if zostaje w AI4.1. Oszczędność kwotowa = AI1.3.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak przebiegów what-if.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              run_code: "Kod",
              baseline_label: "Punkt",
              levers_label: "Dźwignie",
              result_label: "Wynik",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj przebiegu…"
            tableKey={BUSINESS_LISTS.counterfactualRun.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <CounterfactualRunComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
