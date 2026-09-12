import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadInventoryPositionMarks,
  type InventoryPositionMarkRow,
} from "@/lib/inventory-position-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { InventoryPositionComposer } from "./mark-form"

const col = createColumnHelper<InventoryPositionMarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("stock_kind", { header: "Tryb stock" }),
  col.accessor("source_ref", { header: "Zrodlo" }),
]

export function InventoryPositionBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const rows = useQuery({
    enabled: ready,
    queryFn: loadInventoryPositionMarks,
    queryKey: ["inventory-position-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-ip="board">
      <CatalogHeading
        title="Inventory position"
        subtitle="EXP3.3 · position|plant|sku · bez WMS"
      />
      {!ready ? (
        <TenantSessionNotice />
      ) : (
        <InventoryPositionComposer organizationId={orgId} />
      )}
      {rows.error ? <CatalogError error={rows.error} /> : null}
      {ready && rows.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            stock_kind: "Tryb stock",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={rows.data ?? []}
          globalFilterPlaceholder="Szukaj inventory position…"
          tableKey={BUSINESS_LISTS.inventoryPositionMark.tableKey}
        />
      ) : null}
    </section>
  )
}
