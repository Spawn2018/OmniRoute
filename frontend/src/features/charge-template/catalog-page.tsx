import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { BundleSlotPanel } from "./bundle-form"

export function BundleDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-charge-template="desk">
      <CatalogHeading
        title="Szablony opłat"
        subtitle="P2 charge_template · kolekcja kodów + daty · exclusion w SQL"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <BundleSlotPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
