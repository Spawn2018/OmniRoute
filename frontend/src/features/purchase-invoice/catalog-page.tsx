import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchPurchaseInvoices,
  type PurchaseInvoiceRow,
} from "@/lib/purchase-invoices-api"
import { getTenantContext } from "@/lib/tenant"
import { PurchaseInvoiceSave } from "./mark-form"

const helper = createColumnHelper<PurchaseInvoiceRow>()

const COLUMNS = [
  helper.accessor("invoice_ref", { header: "Numer" }),
  helper.accessor("invoice_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function PurchaseInvoiceDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchPurchaseInvoices,
    queryKey: ["purchase-invoices", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-purchase-invoice="board">
      <CatalogHeading
        title="Faktura zakupu"
        subtitle="F10 purchase_invoice · katalog HITL · nie ranking · nie allocation"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PurchaseInvoiceSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            invoice_ref: "Numer",
            invoice_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj FV zakupu…"
          tableKey={BUSINESS_LISTS.purchaseInvoice.tableKey}
        />
      ) : null}
    </section>
  )
}
