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
  loadEmptyDepotMarks,
  type EmptyDepotMarkRow,
} from "@/lib/empty-depot-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { EmptyDepotMarkComposer } from "./mark-form"

const helper = createColumnHelper<EmptyDepotMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod depot" }),
  helper.accessor("depot_kind", { header: "Empty / chassis" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function EmptyDepotMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const canLoad = Boolean(orgId && ctx.userId)
  const query = useQuery({
    enabled: canLoad,
    queryFn: loadEmptyDepotMarks,
    queryKey: ["empty-depot-marks", orgId],
    retry: false,
  })
  const marks = query.data ?? []
  const showTable = canLoad && query.error == null

  return (
    <section
      className="space-y-5 rounded-md border border-stone-800/20 bg-stone-50/50 p-4 dark:bg-stone-950/25"
      data-ed="board"
    >
      <CatalogHeading
        title="Empty / depot / chassis"
        subtitle="EXP4.6 · depot_kind empty|depot|chassis|other · bez live API"
      />
      <p className="text-xs leading-relaxed text-muted-foreground">
        Znacznik empty/depot. Nie yard WMS i nie scrape.
      </p>
      {!canLoad ? (
        <TenantSessionNotice />
      ) : (
        <EmptyDepotMarkComposer organizationId={orgId} />
      )}
      {query.error ? <CatalogError error={query.error} /> : null}
      {showTable && marks.length === 0 ? (
        <p className="rounded border border-dashed border-stone-700/30 p-2 text-sm text-muted-foreground">
          Brak znaczników depot — dodaj pierwszy wpis HITL.
        </p>
      ) : null}
      {showTable ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod depot",
            depot_kind: "Empty / chassis",
            source_ref: "Źródło",
          }}
          columns={COLS}
          data={marks}
          globalFilterPlaceholder="Filtr empty/depot…"
          tableKey={BUSINESS_LISTS.emptyDepotMark.tableKey}
        />
      ) : null}
    </section>
  )
}
