import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchProductTicketMarks,
  type ProductTicketMarkRow,
} from "@/lib/product-ticket-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ProductTicketMarkSave } from "./mark-form"

const col = createColumnHelper<ProductTicketMarkRow>()

export function ProductTicketMarkDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const sessionOk = Boolean(org && tenant.userId)
  const rows = useQuery({
    enabled: sessionOk,
    queryFn: fetchProductTicketMarks,
    queryKey: ["product-ticket-marks", org],
    retry: false,
  })
  const tableCols = [
    col.accessor("mark_code", { header: "Oznaczenie" }),
    col.accessor("ticket_kind", { header: "Rodzaj" }),
    col.accessor("source_ref", { header: "Pochodzenie" }),
  ]

  return (
    <main className="space-y-5 p-1" data-product-ticket="desk">
      <CatalogHeading
        title="Ticket produktu"
        subtitle="Plat-HD · report / triage / owner_ok · bez CAPA, auto-naprawy i operator_notice"
      />
      {sessionOk ? null : <TenantSessionNotice />}
      {rows.error ? <CatalogError error={rows.error} /> : null}
      {sessionOk && !rows.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            ticket_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={tableCols}
          data={rows.data ?? []}
          globalFilterPlaceholder="Szukaj ticketu…"
          tableKey={BUSINESS_LISTS.productTicketMark.tableKey}
        />
      ) : null}
      {sessionOk ? <ProductTicketMarkSave organizationId={org} /> : null}
    </main>
  )
}
