import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchPorts, oceanLclPorts } from "@/lib/ports-api"
import { getTenantContext } from "@/lib/tenant"

export function OceanLclPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const ports = useQuery({
    queryKey: ["ocean-lcl-ports", ctx.organizationId],
    queryFn: () => fetchPorts(""),
    enabled: ready,
    retry: false,
  })
  const sea = oceanLclPorts(ports.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-ocean-lcl="board">
      <CatalogHeading
        title="Drobnica morska"
        subtitle="ocean_lcl M-51 · port.is_seaport · nie tabela LCL · nie CFS"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ports.isError ? <CatalogError error={ports.error} /> : null}
      <ul>
        {sea.map((row) => (
          <li key={row.id} className="text-xs">
            {row.unlocode} {row.name} {row.country_code}{" "}
            <Link className="underline" to="/ports">
              port
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
