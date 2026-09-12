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
  loadDemoSimMarks,
  type DemoSimMarkRow,
} from "@/lib/demo-sim-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { DemoSimMarkComposer } from "./mark-form"

const helper = createColumnHelper<DemoSimMarkRow>()
const COLS = [
  helper.accessor("sim_kind", { header: "Sim" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function DemoSimMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadDemoSimMarks,
    queryKey: ["demo-sim-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-dsm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Znacznik demo sim"
          subtitle="Demo-1b · fleet_150|months_10|other · bez live sim"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik demo sim — tylko katalog danych.</li>
          <li>Bez generatora 150 aut i bez live symulacji floty.</li>
          <li>Odrębny od demo_wipe_mark — postawa sim, nie wipe.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow demo sim.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              sim_kind: "Sim",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika demo sim…"
            tableKey={BUSINESS_LISTS.demoSimMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <DemoSimMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
