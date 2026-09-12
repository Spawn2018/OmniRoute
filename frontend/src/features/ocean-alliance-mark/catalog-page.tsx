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
  loadOceanAllianceMarks,
  type OceanAllianceMarkRow,
} from "@/lib/ocean-alliance-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { OceanAllianceMarkComposer } from "./mark-form"

const helper = createColumnHelper<OceanAllianceMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod alliance" }),
  helper.accessor("ocean_kind", { header: "Alliance / feeder" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function OceanAllianceMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const canLoad = Boolean(orgId && ctx.userId)
  const query = useQuery({
    enabled: canLoad,
    queryFn: loadOceanAllianceMarks,
    queryKey: ["ocean-alliance-marks", orgId],
    retry: false,
  })
  const marks = query.data ?? []
  const showTable = canLoad && query.error == null

  return (
    <section
      className="space-y-5 rounded-md border border-cyan-900/20 bg-cyan-50/35 p-4 dark:bg-cyan-950/20"
      data-oa="board"
    >
      <CatalogHeading
        title="Ocean alliance / feeder"
        subtitle="EXP4.3 · ocean_kind alliance|feeder|slot|other · bez live API"
      />
      <p className="text-xs leading-relaxed text-muted-foreground">
        Znacznik sojuszu/feedera. Nie scrape i nie TEU.
      </p>
      {!canLoad ? (
        <TenantSessionNotice />
      ) : (
        <OceanAllianceMarkComposer organizationId={orgId} />
      )}
      {query.error ? <CatalogError error={query.error} /> : null}
      {showTable && marks.length === 0 ? (
        <p className="rounded border border-dashed border-cyan-800/30 p-2 text-sm text-muted-foreground">
          Brak znaczników ocean — dodaj pierwszy wpis HITL.
        </p>
      ) : null}
      {showTable ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod alliance",
            ocean_kind: "Alliance / feeder",
            source_ref: "Źródło",
          }}
          columns={COLS}
          data={marks}
          globalFilterPlaceholder="Filtr ocean alliance…"
          tableKey={BUSINESS_LISTS.oceanAllianceMark.tableKey}
        />
      ) : null}
    </section>
  )
}
