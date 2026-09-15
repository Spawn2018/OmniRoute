import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { loadAllocationLevels, type AllocationLevelRow } from "@/lib/allocation-levels-api"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"
import { AllocationLevelComposer } from "./ledger-form"

const helper = createColumnHelper<AllocationLevelRow>()
const COLS = [
  helper.accessor("level_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function AllocationLevelBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadAllocationLevels,
    queryKey: ["allocation-levels", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div
      className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]"
      data-allocation-level="desk"
    >
      <section className="space-y-3 border-r border-teal-800/20 pr-4">
        <CatalogHeading
          title="Poziom alokacji"
          subtitle="AI7.0 · level_code · bez CHECK 12"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL otwarty słownik — nowy poziom to nowy wiersz.</li>
          <li>Brak listy 12 poziomów w CHECK. Marża zostaje na charge.</li>
          <li>Bez SQL alokacji i bez TRUE CONTRIBUTION MARGIN w tym plasterze.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak poziomow alokacji.</p>
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
            tableKey={BUSINESS_LISTS.allocationLevel.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <AllocationLevelComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
