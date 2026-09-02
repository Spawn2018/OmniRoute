import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { fetchQuotations, quotationAcceptancePending } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_QUOTE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

export function ShipmentDocumentPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const quotations = useQuery({
    queryKey: ["shipment-document-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_QUOTE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const rows = quotationAcceptancePending(quotations.data ?? [])

  return (
    <div className="flex flex-col gap-4" data-shipment-document="board">
      <CatalogHeading
        title="Dokumenty zlecenia"
        subtitle="shipment_document M-38 · source_ref wyceny · nie PDF · nie HBL"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      {rows.map((row) => (
        <p key={row.id} className="text-xs">
          <Link className="underline" to="/shipments">
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
