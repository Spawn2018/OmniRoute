import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { fetchChannelQuotes } from "@/lib/channel-quotes-api"
import { fetchQuotations, quotationCarrierInquiries, quotationLanes } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_QUOTE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

export function EdiMessagePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const quotations = useQuery({
    queryKey: ["edi-message-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_QUOTE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const quotes = useQuery({
    queryKey: ["edi-message-channel-quotes", ctx.organizationId],
    queryFn: fetchChannelQuotes,
    enabled: ready,
    retry: false,
  })
  const rows = quotationCarrierInquiries(quotationLanes(quotations.data ?? []), quotes.data ?? [])

  return (
    <div className="flex flex-col gap-4" data-edi-message="board">
      <CatalogHeading
        title="EDI"
        subtitle="edi_message M-39 · channel_quote na lane · nie X12 · nie live HTTP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      {quotes.isError ? <CatalogError error={quotes.error} /> : null}
      {rows.map((row) => (
        <p key={row.id} className="text-xs">
          <Link className="underline" to="/channel-quotes">
            {row.source_ref}
          </Link>{" "}
          <Money amount={row.amount} currency={row.currency} />{" "}
          <Link className="underline" to="/quotations">
            quotation
          </Link>
        </p>
      ))}
    </div>
  )
}
