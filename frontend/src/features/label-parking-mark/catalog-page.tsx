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
  loadLabelParkingMarks,
  type LabelParkingMarkRow,
} from "@/lib/label-parking-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LabelParkingMarkComposer } from "./mark-form"

const helper = createColumnHelper<LabelParkingMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod parkingu" }),
  helper.accessor("parking_kind", { header: "secure / labeled" }),
  helper.accessor("source_ref", { header: "Wskazanie" }),
]

export function LabelParkingMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listing = useQuery({
    enabled: ready,
    queryFn: loadLabelParkingMarks,
    queryKey: ["label-parking-marks", orgId],
    retry: false,
  })
  const rows = listing.data ?? []
  const tableOk = ready && listing.error == null

  return (
    <main
      className="mx-auto flex max-w-5xl flex-col gap-6 border-l-4 border-amber-700/50 bg-amber-50/20 px-4 py-6 dark:bg-amber-950/10"
      data-lp="panel"
    >
      <header className="space-y-1">
        <CatalogHeading
          title="LABEL parking"
          subtitle="EXP4.12 · secure|labeled|other · bez mapa GPS"
        />
        <p className="max-w-2xl text-sm text-muted-foreground">
          Znacznik parkingu etykietowanego / secure jako dana HITL. Bez live API i bez
          geofence.
        </p>
      </header>
      <div className="grid gap-4 lg:grid-cols-[minmax(0,18rem)_1fr]">
        <aside className="space-y-3 rounded-md border border-amber-800/30 bg-background p-3">
          {!ready ? <TenantSessionNotice /> : <LabelParkingMarkComposer organizationId={orgId} />}
        </aside>
        <div className="min-w-0 space-y-3">
          {listing.error ? <CatalogError error={listing.error} /> : null}
          {tableOk && rows.length === 0 ? (
            <p className="text-sm text-muted-foreground">Brak znacznikow LABEL parking.</p>
          ) : null}
          {tableOk ? (
            <DataTableShell
              columnLabels={{
                mark_code: "Kod parkingu",
                parking_kind: "secure / labeled",
                source_ref: "Wskazanie",
              }}
              columns={COLS}
              data={rows}
              globalFilterPlaceholder="Filtr parkingu…"
              tableKey={BUSINESS_LISTS.labelParkingMark.tableKey}
            />
          ) : null}
        </div>
      </div>
    </main>
  )
}
