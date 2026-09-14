import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchQualityDescentMarks,
  type QualityDescentMarkRow,
} from "@/lib/quality-descent-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { QualityDescentMarkSave } from "./mark-form"

const helper = createColumnHelper<QualityDescentMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("descent_kind", { header: "Powód" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function QualityDescentMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchQualityDescentMarks,
    queryKey: ["quality-descent-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-quality-descent-mark="board">
      <CatalogHeading
        title="ZEJŚCIE JAKOŚCI"
        subtitle="AI8.2 quality_descent_mark · HITL mae/crps/brier/manual · nie silnik · nie L3 write"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <QualityDescentMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            descent_kind: "Powód",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj powody zejścia…"
          tableKey={BUSINESS_LISTS.qualityDescentMark.tableKey}
        />
      ) : null}
    </section>
  )
}
