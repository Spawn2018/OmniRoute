import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchPorts, railPorts } from "@/lib/ports-api"
import { getTenantContext } from "@/lib/tenant"

export function IntermodalRailPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const ports = useQuery({
    queryKey: ["intermodal-rail-ports", ctx.organizationId],
    queryFn: () => fetchPorts(""),
    enabled: ready,
    retry: false,
  })
  const rail = railPorts(ports.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-intermodal-rail="board">
      <CatalogHeading
        title="Kolej intermodalna"
        subtitle="intermodal_rail M-49 · port.function_flags rail · nie wagon · nie CIM"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ports.isError ? <CatalogError error={ports.error} /> : null}
      <ul>
        {rail.map((row) => (
          <li key={row.id} className="text-xs">
            {row.unlocode} {row.name} {row.function_flags.join(" ")}{" "}
            <Link className="underline" to="/ports">
              port
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
