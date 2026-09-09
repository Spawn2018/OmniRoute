import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { ImpactPanel } from "./impact-form"

export function ImpactDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tower-impact="desk">
      <CatalogHeading
        title="Skutek wieży"
        subtitle="V6 tower_impact · etap łańcucha + umowa · nie silnik EBITDA"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ImpactPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
