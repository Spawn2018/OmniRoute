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
  loadFuelCardMarks,
  type FuelCardMarkRow,
} from "@/lib/fuel-card-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FuelCardMarkComposer } from "./mark-form"

const helper = createColumnHelper<FuelCardMarkRow>()
const COLS = [
  helper.accessor("card_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function FuelCardMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadFuelCardMarks,
    queryKey: ["fuel-card-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-fcm="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="Fuel card"
          subtitle="EXP2.14 · fuel|anomaly|other · bez live"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik karty paliwowej — tylko katalog danych.</li>
          <li>Bez litrów, kwot i silnika anomalii SQL.</li>
          <li>Bez live fuel card API.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow fuel card.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              card_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj fuel card…"
            tableKey={BUSINESS_LISTS.fuelCardMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <FuelCardMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
