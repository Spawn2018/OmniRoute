import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchInventoryFinanceMarks,
  type InventoryFinanceMarkRow,
} from "@/lib/inventory-finance-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { InventoryFinanceMarkSave } from "./mark-form"

const helper = createColumnHelper<InventoryFinanceMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("finance_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function InventoryFinanceMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchInventoryFinanceMarks,
    queryKey: ["inventory-finance-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-inventory-finance-mark="board">
      <CatalogHeading
        title="Zapas finansowy"
        subtitle="BR1.2 inventory_finance_mark · katalog HITL · nie wycena SQL · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <InventoryFinanceMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            finance_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znaczników zapasu…"
          tableKey={BUSINESS_LISTS.inventoryFinanceMark.tableKey}
        />
      ) : null}
    </section>
  )
}
