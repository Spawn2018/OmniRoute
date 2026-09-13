import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchRoutePlanMarks, type RoutePlanMarkRow } from "@/lib/route-plan-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { RoutePlanMarkSave } from "./mark-form"

const helper = createColumnHelper<RoutePlanMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("plan_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function RoutePlanMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchRoutePlanMarks,
    queryKey: ["route-plan-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-route-plan-mark="board">
      <CatalogHeading
        title="Znacznik planu trasy"
        subtitle="BR3.0 route_plan_mark · katalog HITL · nie Valhalla · nie km"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <RoutePlanMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            plan_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika planu trasy…"
          tableKey={BUSINESS_LISTS.routePlanMark.tableKey}
        />
      ) : null}
    </section>
  )
}
