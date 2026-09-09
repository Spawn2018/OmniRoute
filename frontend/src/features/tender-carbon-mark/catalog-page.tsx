import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { CarbonPanel } from "./mark-form"

export function CarbonDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-carbon-mark="desk">
      <CatalogHeading
        title="Ślad węglowy przetargu"
        subtitle="G2.14 tender_carbon_mark · declared/exempt + source_ref · nie kalkulator kg"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CarbonPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
