import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchTenancyUsers, gdprSubjects } from "@/lib/api"
import { getTenantContext } from "@/lib/tenant"

export function GdprPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const users = useQuery({
    queryKey: ["gdpr-users", ctx.organizationId],
    queryFn: fetchTenancyUsers,
    enabled: ready,
    retry: false,
  })
  const rows = gdprSubjects(users.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-gdpr="board">
      <CatalogHeading
        title="RODO"
        subtitle="gdpr M-56 · app_user email · nie wniosek · nie usuwanie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {users.isError ? <CatalogError error={users.error} /> : null}
      <ul>
        {rows.map((row) => (
          <li key={row.id} className="text-xs">
            {row.email} {row.display_name}{" "}
            <Link className="underline" to="/tenancy/users">
              konto
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
