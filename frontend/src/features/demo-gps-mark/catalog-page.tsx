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
  loadDemoGpsMarks,
  type DemoGpsMarkRow,
} from "@/lib/demo-gps-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { DemoGpsMarkComposer } from "./mark-form"

const helper = createColumnHelper<DemoGpsMarkRow>()
const COLS = [
  helper.accessor("demo_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function DemoGpsMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadDemoGpsMarks,
    queryKey: ["demo-gps-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-dgm="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="Demo GPS"
          subtitle="EXP0.11 · seven_day|fleet_demo|other · bez live GPS"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik demo GPS — tylko katalog danych.</li>
          <li>Bez live poll, lat/lng i wipe demo.</li>
          <li>Bez kwoty i marży.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow demo GPS.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              demo_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj demo GPS…"
            tableKey={BUSINESS_LISTS.demoGpsMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <DemoGpsMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
