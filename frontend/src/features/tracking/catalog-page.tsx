import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchPorts } from "@/lib/ports-api"
import { fetchQuotations, quotationLanes } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_QUOTE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

function unlocodeById(ports: readonly { id: string; unlocode: string }[], id: string): string {
  for (const port of ports) {
    if (port.id === id) {
      return port.unlocode
    }
  }
  return id
}

export function TrackingPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const quotations = useQuery({
    queryKey: ["tracking-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_QUOTE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const ports = useQuery({
    queryKey: ["tracking-ports", ctx.organizationId],
    queryFn: () => fetchPorts(""),
    enabled: ready,
    retry: false,
  })
  const lanes = quotationLanes(quotations.data ?? [])
  const catalog = ports.data ?? []

  return (
    <div className="flex flex-col gap-4" data-tracking="board">
      <CatalogHeading
        title="Tracking"
        subtitle="tracking M-36 · lane POL/POD · nie AIS · nie mapa"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      {ports.isError ? <CatalogError error={ports.error} /> : null}
      {lanes.map((lane) => (
        <p key={lane.id} className="text-xs">
          <Link className="underline" to="/shipments">
            {lane.chargeCode}
          </Link>{" "}
          {unlocodeById(catalog, lane.originPortId)} → {unlocodeById(catalog, lane.destinationPortId)}{" "}
          <Link className="underline" to="/quotations">
            quotation
          </Link>
        </p>
      ))}
    </div>
  )
}
