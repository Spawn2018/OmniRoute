import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { loadAllocationKeys, type AllocationKeyRow } from "@/lib/allocation-keys-api"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"
import { AllocationKeyComposer } from "./ledger-form"

const helper = createColumnHelper<AllocationKeyRow>()
const COLS = [
  helper.accessor("key_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function AllocationKeyBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadAllocationKeys,
    queryKey: ["allocation-keys", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div
      className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]"
      data-allocation-key="desk"
    >
      <section className="space-y-3 border-r border-teal-800/20 pr-4">
        <CatalogHeading
          title="Klucz alokacji"
          subtitle="AI7.0 · key_code · bez CHECK 23"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL otwarty słownik — nowy klucz to nowy wiersz.</li>
          <li>Brak listy 23 kluczy w CHECK. Marża zostaje na charge.</li>
          <li>Bez SQL alokacji i bez TRUE CONTRIBUTION MARGIN w tym plasterze.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak kluczy alokacji.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              key_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj klucza…"
            tableKey={BUSINESS_LISTS.allocationKey.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <AllocationKeyComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
