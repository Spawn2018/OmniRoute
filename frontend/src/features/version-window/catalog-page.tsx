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
  loadVersionWindows,
  type VersionWindowRow,
} from "@/lib/version-windows-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<VersionWindowRow>()
const COLS = [
  helper.accessor("model_version", { header: "Wersja" }),
  helper.accessor("created_on", { header: "Dzień UTC" }),
  helper.accessor("pair_count", { header: "Pary" }),
  helper.accessor("avg_mae", { header: "Śr. MAE" }),
  helper.accessor("avg_crps", { header: "Śr. CRPS" }),
]

export function VersionWindowBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadVersionWindows,
    queryKey: ["version-windows", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="space-y-3" data-version-window="desk">
      <CatalogHeading
        title="Wynik okna wersji"
        subtitle="AI2.1 · średnie MAE/CRPS per model_version i dzień UTC · liczy Postgres"
      />
      <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
        <li>Szereg dzienny ze złączenia par. Bez progu i bez flagi dryfu.</li>
        <li>Średnie przychodzą z widoku SQL. Nie wpisujesz ich z formularza.</li>
        <li>Przełączenie modelu zostaje poza tym ekranem.</li>
      </ul>
      {!sessionReady ? <TenantSessionNotice /> : null}
      {query.error ? <CatalogError error={query.error} /> : null}
      {showTable && catalog.length === 0 ? (
        <p className="text-sm text-muted-foreground">Brak sparowanych dni do porównania.</p>
      ) : null}
      {showTable ? (
        <DataTableShell
          columnLabels={{
            model_version: "Wersja",
            created_on: "Dzień UTC",
            pair_count: "Pary",
            avg_mae: "Śr. MAE",
            avg_crps: "Śr. CRPS",
          }}
          columns={COLS}
          data={catalog}
          globalFilterPlaceholder="Szukaj wersji albo dnia…"
          tableKey={BUSINESS_LISTS.versionWindow.tableKey}
        />
      ) : null}
    </div>
  )
}
