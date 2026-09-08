import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { IndexMarkPanel } from "./index-form"

export function IndexDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-fuel-index="desk">
      <CatalogHeading
        title="Indeksy paliwowe"
        subtitle="P3 fuel_index · FSC/BAF/CAF jako dane · nie mnożenie na charge"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <IndexMarkPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
