import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCostCategoryMarks, type CostCategoryMarkRow } from "@/lib/cost-category-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CostCategoryMarkSave } from "./mark-form"

const column = createColumnHelper<CostCategoryMarkRow>()

const TABLE_COLUMNS = [
  column.accessor("mark_code", { header: "Kod" }),
  column.accessor("category_kind", { header: "Kategoria" }),
  column.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CostCategoryMarkDesk() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const board = useQuery({
    enabled: sessionReady,
    queryFn: fetchCostCategoryMarks,
    queryKey: ["cost-category-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-cost-category-mark="board">
      <CatalogHeading
        title="Cost category"
        subtitle="AI7.0 · HITL cost_category_mark · etykieta category_kind · bez allocation SQL"
      />
      {!sessionReady ? <TenantSessionNotice /> : null}
      {sessionReady ? <CostCategoryMarkSave organizationId={organizationId} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {sessionReady && !board.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            category_kind: "Kategoria",
            source_ref: "Pochodzenie",
          }}
          columns={TABLE_COLUMNS}
          data={board.data ?? []}
          globalFilterPlaceholder="Filtruj cost category…"
          tableKey={BUSINESS_LISTS.costCategoryMark.tableKey}
        />
      ) : null}
    </section>
  )
}
