import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchParties, sanctionsParties } from "@/lib/parties-api"
import { getTenantContext } from "@/lib/tenant"

export function SanctionsPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const parties = useQuery({
    queryKey: ["sanctions-parties", ctx.organizationId],
    queryFn: fetchParties,
    enabled: ready,
    retry: false,
  })
  const rows = sanctionsParties(parties.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-sanctions="board">
      <CatalogHeading
        title="Sankcje"
        subtitle="sanctions M-53 · party aktywny · tax_id i kraj · nie OFAC · nie HTTP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {parties.isError ? <CatalogError error={parties.error} /> : null}
      <ul>
        {rows.map((row) => (
          <li key={row.id} className="text-xs">
            {row.legal_name} {row.tax_id ?? "—"} {row.country_code}{" "}
            <Link className="underline" to="/parties">
              kontrahent
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
