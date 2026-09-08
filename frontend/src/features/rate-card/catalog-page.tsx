import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { WhenTokenPanel } from "./when-form"

export function WhenDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-rate-card="desk">
      <CatalogHeading
        title="Karty stawek"
        subtitle="P1 rate_card · applies_when jako dane · nie silnik WHEN/IF"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <WhenTokenPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
