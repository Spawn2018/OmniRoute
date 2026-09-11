import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchLoadPlanMarks, type LoadPlanMarkRow } from "@/lib/load-plan-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LoadPlanMarkSave } from "./mark-form"

const helper = createColumnHelper<LoadPlanMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("stance_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function LoadPlanMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchLoadPlanMarks,
    queryKey: ["load-plan-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-load-plan-mark="board">
      <CatalogHeading
        title="Znacznik planu załadunku"
        subtitle="G6 load_plan_mark · katalog HITL · nie solver OR · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <LoadPlanMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            stance_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika planu załadunku…"
          tableKey={BUSINESS_LISTS.loadPlanMark.tableKey}
        />
      ) : null}
    </section>
  )
}
