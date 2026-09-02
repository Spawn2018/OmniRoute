import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { fetchCharges } from "@/lib/charges-api"
import { fetchQuotations, quotationInvoiceSettlements } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_LANE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

export function QuoteInvoiceSettlementPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const quotations = useQuery({
    queryKey: ["quote-invoice-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_LANE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const charges = useQuery({
    queryKey: ["quote-invoice-charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: ready,
    retry: false,
  })
  const settlements = quotationInvoiceSettlements(quotations.data ?? [], charges.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-quote-invoice-settlement="board">
      <CatalogHeading
        title="Rozliczenie wyceny"
        subtitle="quote_invoice_settlement M-41 · sell z charge po rate_line_id · nie tabela · nie odejmowanie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      {charges.isError ? <CatalogError error={charges.error} /> : null}
      <ul>
        {settlements.map((row) => (
          <li key={row.rateLineId} className="text-xs">
            {row.quotations.map((quotation) => (
              <span key={quotation.id}>
                {quotation.charge_code}{" "}
                <Money amount={quotation.amount} currency={quotation.currency} />
              </span>
            ))}
            {" · "}
            {row.charges.map((charge) => (
              <span key={charge.id}>
                <Money amount={charge.sell_amount} currency={charge.sell_currency} />
              </span>
            ))}
            {" · "}
            <Link className="underline" to="/quotations">
              wycena
            </Link>
            {" · "}
            <Link className="underline" to="/invoices">
              faktura
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
