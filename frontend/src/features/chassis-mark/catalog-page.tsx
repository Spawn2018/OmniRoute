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
  loadChassisMarks,
  type ChassisMarkRow,
} from "@/lib/chassis-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ChassisMarkComposer } from "./mark-form"

const helper = createColumnHelper<ChassisMarkRow>()
const COLS = [
  helper.accessor("chassis_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function ChassisMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadChassisMarks,
    queryKey: ["chassis-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-chm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Chassis / trailer"
          subtitle="EXP4.5b · chassis|trailer|other · bez live"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik chassis/trailer — tylko katalog danych.</li>
          <li>Bez TEU, kwot i live chassis pool.</li>
          <li>Bez yard live i WMS — obok empty_depot_mark.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow chassis/trailer.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              chassis_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj chassis/trailer…"
            tableKey={BUSINESS_LISTS.chassisMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <ChassisMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
