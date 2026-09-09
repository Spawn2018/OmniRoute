import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { MethodPanel } from "./method-form"

export function MethodDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-carbon-method="desk">
      <CatalogHeading
        title="Metodyka CO₂"
        subtitle="C5 carbon_method · kod + wersja + source_ref · nie kg"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <MethodPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
