import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { chinaRailPorts, fetchPorts } from "@/lib/ports-api"
import { getTenantContext } from "@/lib/tenant"
import { ChinaRailLegBoard } from "./china-rail-leg-board"

export function ChinaRailPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const ports = useQuery({
    queryKey: ["china-rail-ports", ctx.organizationId],
    queryFn: () => fetchPorts(""),
    enabled: ready,
    retry: false,
  })
  const china = chinaRailPorts(ports.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-china-rail="board">
      <CatalogHeading
        title="Kolej z Chin"
        subtitle="china_rail M-50 · odcinek shipment_leg china_rail · nie korytarz · nie HTTP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ports.isError ? <CatalogError error={ports.error} /> : null}
      <ul>
        {china.map((row) => (
          <li key={row.id} className="text-xs">
            {row.unlocode} {row.name} {row.country_code}{" "}
            <Link className="underline" to="/rail">
              kolej
            </Link>{" "}
            <Link className="underline" to="/ports">
              port
            </Link>
          </li>
        ))}
      </ul>
      {ready ? <ChinaRailLegBoard organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
