import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Money } from "@/components/money"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadMarginFloors,
  type MarginFloorRow,
} from "@/lib/margin-floors-api"
import { getTenantContext } from "@/lib/tenant"
import { MarginFloorComposer } from "./floor-form"

const helper = createColumnHelper<MarginFloorRow>()
const COLS = [
  helper.accessor("floor_code", { header: "Kod" }),
  helper.accessor("origin_unlocode", { header: "Origin" }),
  helper.accessor("destination_unlocode", { header: "Dest" }),
  helper.display({
    id: "floor_amount",
    header: "Podłoga",
    cell: (info) => (
      <Money
        amount={info.row.original.floor_amount}
        currency={info.row.original.floor_currency}
      />
    ),
  }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function MarginFloorBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadMarginFloors,
    queryKey: ["margin-floors", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div
      className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]"
      data-margin-floor="desk"
    >
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Podłoga marży"
          subtitle="N6 · Decimal + para UN/LOCODE · bez 409 na charge"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL katalog minimalnej marży na korytarzu — operator wpisuje kwotę.</li>
          <li>Para UN/LOCODE to dana. Egzekucja 409 przy zapisie charge to leftover.</li>
          <li>Marża zostaje na charge. Serwis nie liczy sell−buy.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak wierszy podłogi marży.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              floor_code: "Kod",
              origin_unlocode: "Origin",
              destination_unlocode: "Dest",
              floor_amount: "Podłoga",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj podłogi…"
            tableKey={BUSINESS_LISTS.marginFloor.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <MarginFloorComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
