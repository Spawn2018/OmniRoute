import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadTwinKinds, type TwinKindRow } from "@/lib/twin-kinds-api"
import { getTenantContext } from "@/lib/tenant"
import { TwinKindComposer } from "./ledger-form"

const helper = createColumnHelper<TwinKindRow>()
const COLS = [
  helper.accessor("kind_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function TwinKindBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadTwinKinds,
    queryKey: ["twin-kinds", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div
      className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]"
      data-twin-kind="desk"
    >
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Rodzaj bliźniaka"
          subtitle="AI1.4 · kind_code · bez CHECK"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL otwarty słownik — nowy rodzaj to nowy wiersz.</li>
          <li>Brak zamkniętej listy vehicle/driver z twin_mark.</li>
          <li>data_source i autonomy_level zostają następnymi słownikami.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak rodzajów bliźniaka.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              kind_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj rodzaju…"
            tableKey={BUSINESS_LISTS.twinKind.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <TwinKindComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
