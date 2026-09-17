import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchInvoiceMatchMarks,
  type InvoiceMatchMarkRow,
} from "@/lib/invoice-match-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { InvoiceMatchMarkSave } from "./mark-form"

const helper = createColumnHelper<InvoiceMatchMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("match_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function InvoiceMatchMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchInvoiceMatchMarks,
    queryKey: ["invoice-match-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-invoice-match-mark="board">
      <CatalogHeading
        title="Dopasowanie FV zakupu"
        subtitle="F10 invoice_match_mark · katalog HITL · nie ranking SQL · nie allocation"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <InvoiceMatchMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            match_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj match FV…"
          tableKey={BUSINESS_LISTS.invoiceMatchMark.tableKey}
        />
      ) : null}
    </section>
  )
}
