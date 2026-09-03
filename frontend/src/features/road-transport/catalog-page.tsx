import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchLocations, roadLocations } from "@/lib/locations-api"
import { getTenantContext } from "@/lib/tenant"
import { RoadLegBoard } from "./road-leg-board"

export function RoadTransportPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const locations = useQuery({
    queryKey: ["road-transport-locations", ctx.organizationId],
    queryFn: () => fetchLocations(""),
    enabled: ready,
    retry: false,
  })
  const road = roadLocations(locations.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-road-transport="board">
      <CatalogHeading
        title="Transport drogowy"
        subtitle="road_transport M-48 · odcinek shipment_leg road · nie TMS · nie GPS"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {locations.isError ? <CatalogError error={locations.error} /> : null}
      <ul>
        {road.map((row) => (
          <li key={row.id} className="text-xs">
            {row.kind} {row.name} {row.city ?? ""} {row.postal_code ?? ""}{" "}
            <Link className="underline" to="/locations">
              lokalizacja
            </Link>
          </li>
        ))}
      </ul>
      {ready ? <RoadLegBoard organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
