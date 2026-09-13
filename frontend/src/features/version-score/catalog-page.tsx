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
  loadVersionScores,
  type VersionScoreRow,
} from "@/lib/version-scores-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<VersionScoreRow>()
const COLS = [
  helper.accessor("model_version", { header: "Wersja" }),
  helper.accessor("pair_count", { header: "Pary" }),
  helper.accessor("avg_mae", { header: "Śr. MAE" }),
  helper.accessor("avg_crps", { header: "Śr. CRPS" }),
]

export function VersionScoreBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadVersionScores,
    queryKey: ["version-scores", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="space-y-3" data-version-score="desk">
      <CatalogHeading
        title="Wynik wersji"
        subtitle="AI2.1 · średnie MAE/CRPS per model_version · liczy Postgres"
      />
      <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
        <li>Ranking wersji modelu ze złączenia par. Bez przełączania champion.</li>
        <li>Średnie przychodzą z widoku SQL. Nie wpisujesz ich z formularza.</li>
        <li>Dryf i auto-champion zostają poza tym ekranem.</li>
      </ul>
      {!sessionReady ? <TenantSessionNotice /> : null}
      {query.error ? <CatalogError error={query.error} /> : null}
      {showTable && catalog.length === 0 ? (
        <p className="text-sm text-muted-foreground">Brak sparowanych wersji do porównania.</p>
      ) : null}
      {showTable ? (
        <DataTableShell
          columnLabels={{
            model_version: "Wersja",
            pair_count: "Pary",
            avg_mae: "Śr. MAE",
            avg_crps: "Śr. CRPS",
          }}
          columns={COLS}
          data={catalog}
          globalFilterPlaceholder="Szukaj wersji…"
          tableKey={BUSINESS_LISTS.versionScore.tableKey}
        />
      ) : null}
    </div>
  )
}
