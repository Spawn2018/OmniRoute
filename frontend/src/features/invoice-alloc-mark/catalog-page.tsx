import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchInvoiceAllocMarks,
  type InvoiceAllocMarkRow,
} from "@/lib/invoice-alloc-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { InvoiceAllocMarkSave } from "./mark-form"

const helper = createColumnHelper<InvoiceAllocMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("alloc_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function InvoiceAllocMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchInvoiceAllocMarks,
    queryKey: ["invoice-alloc-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-invoice-alloc-mark="board">
      <CatalogHeading
        title="Alokacja FV zakupu"
        subtitle="F10 invoice_alloc_mark · katalog HITL · nie allocation z kwotą · nie ranking"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <InvoiceAllocMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            alloc_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj alokacji FV…"
          tableKey={BUSINESS_LISTS.invoiceAllocMark.tableKey}
        />
      ) : null}
    </section>
  )
}
