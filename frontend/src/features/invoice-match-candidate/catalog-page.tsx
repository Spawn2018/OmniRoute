import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchInvoiceMatchCandidates,
  type InvoiceMatchCandidateRow,
} from "@/lib/invoice-match-candidates-api"
import { getTenantContext } from "@/lib/tenant"
import { InvoiceMatchCandidateSave } from "./mark-form"

const helper = createColumnHelper<InvoiceMatchCandidateRow>()

const COLUMNS = [
  helper.accessor("candidate_code", { header: "Kod" }),
  helper.accessor("candidate_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function InvoiceMatchCandidateDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchInvoiceMatchCandidates,
    queryKey: ["invoice-match-candidates", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-invoice-match-candidate="board">
      <CatalogHeading
        title="Kandydat dopasowania FV"
        subtitle="F10 invoice_match_candidate · katalog HITL · nie live ranking SQL · nie auto-link"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <InvoiceMatchCandidateSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            candidate_code: "Kod",
            candidate_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj kandydata dopasowania FV…"
          tableKey={BUSINESS_LISTS.invoiceMatchCandidate.tableKey}
        />
      ) : null}
    </section>
  )
}
