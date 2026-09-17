import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchProductTickets,
  type ProductTicketRow,
} from "@/lib/product-tickets-api"
import { getTenantContext } from "@/lib/tenant"
import { ProductTicketSave } from "./ticket-form"

const helper = createColumnHelper<ProductTicketRow>()

const COLUMNS = [
  helper.accessor("ticket_code", { header: "Oznaczenie" }),
  helper.accessor("title", { header: "Tytul" }),
  helper.accessor("ticket_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function ProductTicketDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchProductTickets,
    queryKey: ["product-tickets", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-product-ticket="board">
      <CatalogHeading
        title="Ticket produktu"
        subtitle="Plat-HD-flow product_ticket · HITL title/body · nie auto-fix"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <ProductTicketSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            ticket_code: "Oznaczenie",
            title: "Tytul",
            ticket_kind: "Rodzaj",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj tickety produktu…"
          tableKey={BUSINESS_LISTS.productTicket.tableKey}
        />
      ) : null}
    </section>
  )
}
