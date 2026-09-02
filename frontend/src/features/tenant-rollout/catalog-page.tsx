import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { t } from "@/lib/i18n"
import { fetchOrganizationSettings, rolloutSettings } from "@/lib/organization-settings-api"
import { getTenantContext } from "@/lib/tenant"

export function TenantRolloutPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const settings = useQuery({
    queryKey: ["tenant-rollout-settings", ctx.organizationId],
    queryFn: fetchOrganizationSettings,
    enabled: ready,
    retry: false,
  })
  const rows = rolloutSettings(settings.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-tenant-rollout="board">
      <CatalogHeading
        title={t("tenant_rollout.title")}
        subtitle={t("tenant_rollout.subtitle")}
      />
      {!ready ? <TenantSessionNotice /> : null}
      {settings.isError ? <CatalogError error={settings.error} /> : null}
      <ul>
        {rows.map((row) => (
          <li key={row.id} className="text-xs">
            {row.setting_key} {row.setting_value}{" "}
            <Link className="underline" to="/organization-settings">
              ustawienia
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
