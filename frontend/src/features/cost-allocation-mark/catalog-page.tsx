import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCostAllocationMarks, type CostAllocationMarkRow } from "@/lib/cost-allocation-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CostAllocationMarkSave } from "./mark-form"

const column = createColumnHelper<CostAllocationMarkRow>()

const TABLE_COLUMNS = [
  column.accessor("mark_code", { header: "Kod" }),
  column.accessor("alloc_kind", { header: "Rodzaj podziału" }),
  column.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CostAllocationMarkDesk() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const board = useQuery({
    enabled: sessionReady,
    queryFn: fetchCostAllocationMarks,
    queryKey: ["cost-allocation-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-cost-allocation-mark="board">
      <CatalogHeading
        title="Cost allocation"
        subtitle="EXP2.3 · HITL cost_allocation_mark · etykieta alloc_kind · bez allocation SQL"
      />
      {!sessionReady ? <TenantSessionNotice /> : null}
      {sessionReady ? <CostAllocationMarkSave organizationId={organizationId} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {sessionReady && !board.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            alloc_kind: "Rodzaj podziału",
            source_ref: "Pochodzenie",
          }}
          columns={TABLE_COLUMNS}
          data={board.data ?? []}
          globalFilterPlaceholder="Filtruj cost allocation…"
          tableKey={BUSINESS_LISTS.costAllocationMark.tableKey}
        />
      ) : null}
    </section>
  )
}
