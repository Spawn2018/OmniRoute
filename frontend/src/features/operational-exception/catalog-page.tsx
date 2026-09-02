import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchQuotations, quotationOperationalExceptions } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_QUOTE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

function missingLaneLabel(originPortId: string | null, destinationPortId: string | null): string {
  if (originPortId === null && destinationPortId === null) {
    return "brak POL i POD"
  }
  if (originPortId === null) {
    return "brak POL"
  }
  return "brak POD"
}

export function OperationalExceptionPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const quotations = useQuery({
    queryKey: ["operational-exception-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_QUOTE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const rows = quotationOperationalExceptions(quotations.data ?? [])

  return (
    <div className="flex flex-col gap-4" data-operational-exception="board">
      <CatalogHeading
        title="Wyjątki"
        subtitle="operational_exception M-37 · party bez pełnego POL/POD · nie AIS · nie mapa"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      {rows.map((row) => (
        <p key={row.id} className="text-xs">
          <Link className="underline" to="/shipments">
            {row.charge_code}
          </Link>{" "}
          {missingLaneLabel(row.origin_port_id, row.destination_port_id)}{" "}
          <Link className="underline" to="/tracking">
            tracking
          </Link>{" "}
          <Link className="underline" to="/quotations">
            quotation
          </Link>
        </p>
      ))}
    </div>
  )
}
