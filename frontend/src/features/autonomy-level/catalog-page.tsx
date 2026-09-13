import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { loadAutonomyLevels, type AutonomyLevelRow } from "@/lib/autonomy-levels-api"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"
import { AutonomyLevelComposer } from "./ledger-form"

const helper = createColumnHelper<AutonomyLevelRow>()
const COLS = [
  helper.accessor("level_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function AutonomyLevelBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadAutonomyLevels,
    queryKey: ["autonomy-levels", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div
      className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]"
      data-autonomy-level="desk"
    >
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Poziom autonomii"
          subtitle="AI1.4 · level_code · bez CHECK"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL otwarty słownik — nowy poziom to nowy wiersz.</li>
          <li>Brak zamkniętej listy 0–5 z taksonomii B.4.</li>
          <li>data_source (licencja) zostaje w AI5. Brak FK klienta.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak poziomów autonomii.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              level_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj poziomu…"
            tableKey={BUSINESS_LISTS.autonomyLevel.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <AutonomyLevelComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
