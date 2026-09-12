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
  loadThreeWayMarks,
  type ThreeWayMarkRow,
} from "@/lib/three-way-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ThreeWayMarkComposer } from "./mark-form"

const helper = createColumnHelper<ThreeWayMarkRow>()
const COLS = [
  helper.accessor("way_kind", { header: "Strona" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function ThreeWayMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadThreeWayMarks,
    queryKey: ["three-way-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-twm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Znacznik 3-way"
          subtitle="EXP3.3c · buyer|seller|carrier|other · bez tuple"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik 3-way — tylko katalog danych.</li>
          <li>Bez tuple OpenFGA per strona i bez wspólnego SELECT.</li>
          <li>Odrębny od collaboration_mark (CT11) — postawa 3-way EXP3.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow 3-way.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              way_kind: "Strona",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika 3-way…"
            tableKey={BUSINESS_LISTS.threeWayMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <ThreeWayMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
