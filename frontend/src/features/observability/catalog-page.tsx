import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchHealth } from "@/lib/api"
import { getTenantContext } from "@/lib/tenant"

export function ObservabilityPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const health = useQuery({
    queryKey: ["observability-health", ctx.organizationId],
    queryFn: fetchHealth,
    enabled: ready,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-observability="board">
      <CatalogHeading
        title="Obserwowalność"
        subtitle="observability M-68 · fetchHealth · nie OTel · nie k6"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {health.isError ? <CatalogError error={health.error} /> : null}
      {health.data ? (
        <p className="text-xs">
          {health.data.status}{" "}
          <Link className="underline" to="/">
            pulpit
          </Link>
        </p>
      ) : null}
    </section>
  )
}
