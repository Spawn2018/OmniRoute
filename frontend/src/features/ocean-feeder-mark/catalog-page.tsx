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
  loadOceanFeederMarks,
  type OceanFeederMarkRow,
} from "@/lib/ocean-feeder-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { OceanFeederMarkComposer } from "./mark-form"

const helper = createColumnHelper<OceanFeederMarkRow>()
const COLS = [
  helper.accessor("feeder_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function OceanFeederMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadOceanFeederMarks,
    queryKey: ["ocean-feeder-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-ofm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Ocean feeder / short-sea"
          subtitle="EXP4.3b · feeder|short_sea|other · bez live"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik feeder/short-sea — tylko katalog danych.</li>
          <li>Bez TEU, kwot i live feeder schedule.</li>
          <li>Bez AIS i alliance HTTP.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow feeder/short-sea.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              feeder_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj feeder/short-sea…"
            tableKey={BUSINESS_LISTS.oceanFeederMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <OceanFeederMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
