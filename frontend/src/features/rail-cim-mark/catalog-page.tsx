import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadRailCimMarks, type RailCimMarkRow } from "@/lib/rail-cim-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { RailCimMarkComposer } from "./mark-form"

const helper = createColumnHelper<RailCimMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod rail" }),
  helper.accessor("rail_kind", { header: "UIC / CIM / SMGS" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function RailCimMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const canLoad = Boolean(orgId && ctx.userId)
  const query = useQuery({
    enabled: canLoad,
    queryFn: loadRailCimMarks,
    queryKey: ["rail-cim-marks", orgId],
    retry: false,
  })
  const marks = query.data ?? []
  const showTable = canLoad && query.error == null

  return (
    <section
      className="space-y-5 rounded-md border border-amber-900/20 bg-amber-50/40 p-4 dark:bg-amber-950/20"
      data-rcim="board"
    >
      <CatalogHeading
        title="Rail UIC / CIM / SMGS"
        subtitle="EXP4.2 · rail_kind uic|cim|smgs|other · bez live filing"
      />
      <p className="text-xs leading-relaxed text-muted-foreground">
        Znacznik dokumentu kolejowego. Nie scrape CIM i nie km.
      </p>
      {!canLoad ? <TenantSessionNotice /> : <RailCimMarkComposer organizationId={orgId} />}
      {query.error ? <CatalogError error={query.error} /> : null}
      {showTable && marks.length === 0 ? (
        <p className="rounded border border-dashed border-amber-800/30 p-2 text-sm text-muted-foreground">
          Brak znaczników rail — dodaj pierwszy wpis HITL.
        </p>
      ) : null}
      {showTable ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod rail",
            rail_kind: "UIC / CIM / SMGS",
            source_ref: "Źródło",
          }}
          columns={COLS}
          data={marks}
          globalFilterPlaceholder="Filtr rail CIM…"
          tableKey={BUSINESS_LISTS.railCimMark.tableKey}
        />
      ) : null}
    </section>
  )
}
