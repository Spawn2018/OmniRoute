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

const EMPTY_LANE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

export function EdiMessagePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const quotations = useQuery({
    queryKey: ["edi-message-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_LANE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const channelQuotes = useQuery({
    queryKey: ["edi-message-channel-quotes", ctx.organizationId],
    queryFn: fetchChannelQuotes,
    enabled: ready,
    retry: false,
  })
  const matched = quotationCarrierInquiries(
    quotationLanes(quotations.data ?? []),
    channelQuotes.data ?? [],
  )

  return (
    <div className="flex flex-col gap-4" data-edi-message="board">
      <CatalogHeading
        title="EDI"
        subtitle="edi_message M-39 · channel_quote na lane · nie X12 · nie live HTTP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      {channelQuotes.isError ? <CatalogError error={channelQuotes.error} /> : null}
      <ul>
        {matched.map((quote) => (
          <li key={quote.id} className="text-xs">
            {quote.source_ref} <Money amount={quote.amount} currency={quote.currency} />
            {" · "}
            <Link className="underline" to="/channel-quotes">
              kanał
            </Link>
            {" · "}
            <Link className="underline" to="/quotations">
              wycena
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
