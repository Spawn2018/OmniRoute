import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listTimeToFixMarks, type TimeToFixMarkRow } from "@/lib/time-to-fix-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { TimeToFixMarkEditor } from "./mark-form"

const col = createColumnHelper<TimeToFixMarkRow>()

const TABLE = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("fix_kind", { header: "Stan naprawy" }),
  col.accessor("source_ref", { header: "Źródło" }),
]

export function TimeToFixMarkDesk() {
  const session = getTenantContext()
  const org = session.organizationId
  const hasSession = Boolean(org && session.userId)
  const board = useQuery({
    enabled: hasSession,
    queryFn: listTimeToFixMarks,
    queryKey: ["time-to-fix-marks", org],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-ttf="desk">
      <CatalogHeading
        title="TIME-TO-FIX"
        subtitle="EXP2.9 · katalog HITL · fix_kind open/wip/done · bez silnika TTF"
      />
      {!hasSession ? <TenantSessionNotice /> : null}
      {hasSession ? <TimeToFixMarkEditor organizationId={org} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {hasSession && !board.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            fix_kind: "Stan naprawy",
            source_ref: "Źródło",
          }}
          columns={TABLE}
          data={board.data ?? []}
          globalFilterPlaceholder="Szukaj TIME-TO-FIX…"
          tableKey={BUSINESS_LISTS.timeToFixMark.tableKey}
        />
      ) : null}
    </section>
  )
}
