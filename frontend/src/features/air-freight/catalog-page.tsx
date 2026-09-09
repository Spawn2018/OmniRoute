import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { airPorts, fetchPorts } from "@/lib/ports-api"
import { getTenantContext } from "@/lib/tenant"
import { AirwayLegPanel } from "./airway-leg-panel"

export function AirPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const listed = useQuery({
    queryKey: ["air-ports", ctx.organizationId],
    queryFn: () => fetchPorts(""),
    enabled: ready,
    retry: false,
  })
  const airports = airPorts(listed.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-air="run">
      <CatalogHeading
        title="Lotniczy"
        subtitle="air U3 · odcinek shipment_leg air · opcjonalny HAWB/MAWB · nie pula IATA"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <table className="w-full text-xs">
        <tbody>
          {airports.map((row) => (
            <tr key={row.id}>
              <td className="pr-2 font-mono">{row.unlocode}</td>
              <td>{row.name}</td>
              <td>{row.country_code}</td>
              <td>
                <Link className="underline" to="/ports">
                  port
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {ready ? <AirwayLegPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
