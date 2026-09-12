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
  loadRailUicMarks,
  type RailUicMarkRow,
} from "@/lib/rail-uic-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { RailUicMarkComposer } from "./mark-form"

const helper = createColumnHelper<RailUicMarkRow>()
const COLS = [
  helper.accessor("rail_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function RailUicMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadRailUicMarks,
    queryKey: ["rail-uic-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-rum="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="UIC / CIM / SMGS"
          subtitle="EXP4.2 · uic|cim|smgs|other · bez live"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik kolejowy — tylko katalog danych.</li>
          <li>Bez km, kwot i live rail API.</li>
          <li>Bez mapy i wagon live.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow UIC/CIM/SMGS.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              rail_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj UIC/CIM/SMGS…"
            tableKey={BUSINESS_LISTS.railUicMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <RailUicMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
