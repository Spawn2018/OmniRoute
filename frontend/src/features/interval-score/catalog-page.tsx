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
  loadIntervalScores,
  type IntervalScoreRow,
} from "@/lib/interval-scores-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<IntervalScoreRow>()
const COLS = [
  helper.accessor("mae", { header: "MAE" }),
  helper.accessor("crps", { header: "CRPS" }),
  helper.accessor("interval_low", { header: "Dół" }),
  helper.accessor("interval_high", { header: "Góra" }),
  helper.accessor("actual_value", { header: "Fakt" }),
]

export function IntervalScoreBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadIntervalScores,
    queryKey: ["interval-scores", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="space-y-3" data-interval-score="desk">
      <CatalogHeading
        title="Wynik przedziału"
        subtitle="AI2.0 · MAE od środka · CRPS jednostajny · liczy Postgres"
      />
      <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
        <li>Złączenie ledgeru podpowiedzi z ledgerem faktu. Bez zapisu metryki.</li>
        <li>MAE i CRPS przychodzą z widoku SQL. Nie wpisujesz ich z formularza.</li>
        <li>Wpisane CRPS na ledgerze predykcji zostaje osobnym katalogiem.</li>
      </ul>
      {!sessionReady ? <TenantSessionNotice /> : null}
      {query.error ? <CatalogError error={query.error} /> : null}
      {showTable && catalog.length === 0 ? (
        <p className="text-sm text-muted-foreground">Brak sparowanych podpowiedzi i faktów.</p>
      ) : null}
      {showTable ? (
        <DataTableShell
          columnLabels={{
            mae: "MAE",
            crps: "CRPS",
            interval_low: "Dół",
            interval_high: "Góra",
            actual_value: "Fakt",
          }}
          columns={COLS}
          data={catalog}
          globalFilterPlaceholder="Szukaj wyniku przedziału…"
          tableKey={BUSINESS_LISTS.intervalScore.tableKey}
        />
      ) : null}
    </div>
  )
}
