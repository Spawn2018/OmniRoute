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
  loadDemoWipeMarks,
  type DemoWipeMarkRow,
} from "@/lib/demo-wipe-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { DemoWipeMarkComposer } from "./mark-form"

const helper = createColumnHelper<DemoWipeMarkRow>()
const COLS = [
  helper.accessor("wipe_kind", { header: "Wipe" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function DemoWipeMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadDemoWipeMarks,
    queryKey: ["demo-wipe-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-dwm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Znacznik wipe demo"
          subtitle="Demo-1 · usun|retain|other · bez live wipe"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik wipe demo — tylko katalog danych.</li>
          <li>Bez kasowania wierszy tenantów i bez live wipe USUN.</li>
          <li>Odrębny od demo_gps_mark — postawa wipe, nie GPS.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow wipe demo.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              wipe_kind: "Wipe",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika wipe demo…"
            tableKey={BUSINESS_LISTS.demoWipeMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <DemoWipeMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
