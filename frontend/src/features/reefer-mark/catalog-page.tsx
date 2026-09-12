import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadReeferMarks, type ReeferMarkRow } from "@/lib/reefer-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ReeferMarkComposer } from "./mark-form"

const helper = createColumnHelper<ReeferMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod reefer" }),
  helper.accessor("reefer_kind", { header: "Reefer / genset" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function ReeferMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const canLoad = Boolean(orgId && ctx.userId)
  const query = useQuery({
    enabled: canLoad,
    queryFn: loadReeferMarks,
    queryKey: ["reefer-marks", orgId],
    retry: false,
  })
  const marks = query.data ?? []
  const showTable = canLoad && query.error == null

  return (
    <section
      className="space-y-5 rounded-md border border-teal-900/20 bg-teal-50/40 p-4 dark:bg-teal-950/20"
      data-rf="board"
    >
      <CatalogHeading
        title="Reefer / genset"
        subtitle="EXP4.5 · reefer_kind reefer|setpoint|genset|other · bez live API"
      />
      <p className="text-xs leading-relaxed text-muted-foreground">
        Znacznik rodzaju reefer. Nie setpoint SQL i nie scrape.
      </p>
      {!canLoad ? <TenantSessionNotice /> : <ReeferMarkComposer organizationId={orgId} />}
      {query.error ? <CatalogError error={query.error} /> : null}
      {showTable && marks.length === 0 ? (
        <p className="rounded border border-dashed border-teal-800/30 p-2 text-sm text-muted-foreground">
          Brak znaczników reefer — dodaj pierwszy wpis HITL.
        </p>
      ) : null}
      {showTable ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod reefer",
            reefer_kind: "Reefer / genset",
            source_ref: "Źródło",
          }}
          columns={COLS}
          data={marks}
          globalFilterPlaceholder="Filtr reefer…"
          tableKey={BUSINESS_LISTS.reeferMark.tableKey}
        />
      ) : null}
    </section>
  )
}
