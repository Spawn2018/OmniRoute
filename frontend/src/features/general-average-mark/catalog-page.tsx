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
  loadGeneralAverageMarks,
  type GeneralAverageMarkRow,
} from "@/lib/general-average-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { GeneralAverageComposer } from "./mark-form"

const cols = createColumnHelper<GeneralAverageMarkRow>()
const GA_COLS = [
  cols.accessor("mark_code", { header: "Kod GA" }),
  cols.accessor("average_kind", { header: "Rodzaj GA" }),
  cols.accessor("source_ref", { header: "Ref HITL" }),
]

export function GeneralAverageBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ok = Boolean(orgId && ctx.userId)
  const list = useQuery({
    enabled: ok,
    queryFn: loadGeneralAverageMarks,
    queryKey: ["general-average-marks", orgId],
    retry: false,
  })

  return (
    <main className="space-y-4 border-t-4 border-sky-800/50 pt-3" data-ga="desk">
      <CatalogHeading
        title="General average"
        subtitle="EXP3.11 · HITL ga|contribution|sacrifice|other · bez live"
      />
      <p className="text-xs text-muted-foreground">
        Znacznik York-Antwerp jako dana — nie kwota i nie charge.
      </p>
      {ok ? <GeneralAverageComposer organizationId={orgId} /> : <TenantSessionNotice />}
      {list.error ? <CatalogError error={list.error} /> : null}
      {ok && list.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod GA",
            average_kind: "Rodzaj GA",
            source_ref: "Ref HITL",
          }}
          columns={GA_COLS}
          data={list.data ?? []}
          globalFilterPlaceholder="Filtruj general average…"
          tableKey={BUSINESS_LISTS.generalAverageMark.tableKey}
        />
      ) : null}
    </main>
  )
}
