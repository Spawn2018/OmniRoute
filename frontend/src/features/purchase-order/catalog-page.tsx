import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listPurchaseOrders, type PurchaseOrderRow } from "@/lib/purchase-orders-api"
import { getTenantContext } from "@/lib/tenant"
import { PurchaseOrderSave } from "./purchase-order-form"

const cols = createColumnHelper<PurchaseOrderRow>()

const PURCHASE_ORDER_COLUMNS = [
  cols.accessor("po_code", { header: "Kod" }),
  cols.accessor("plant_label", { header: "Zakład" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

const PURCHASE_ORDER_LABELS = {
  po_code: "Kod",
  plant_label: "Zakład",
  source_ref: "Pochodzenie",
}

function PurchaseOrderTable(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listPurchaseOrders,
    queryKey: ["purchase-order-headers", args.organizationId],
    retry: false,
  })
  if (listed.error) {
    return <CatalogError error={listed.error} />
  }
  return (
    <DataTableShell
      columnLabels={PURCHASE_ORDER_LABELS}
      columns={PURCHASE_ORDER_COLUMNS}
      data={listed.data ?? []}
      globalFilterPlaceholder="Filtruj zamówienie zakupu…"
      tableKey={BUSINESS_LISTS.purchaseOrder.tableKey}
    />
  )
}

export function PurchaseOrderDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-5" data-purchase-order="board">
      <CatalogHeading
        title="Zamówienie zakupu"
        subtitle="CT1 purchase_order · nagłówek · nie linia SKU · nie ASN"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="flex flex-col gap-8">
          <PurchaseOrderSave organizationId={ctx.organizationId} />
          <PurchaseOrderTable organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
