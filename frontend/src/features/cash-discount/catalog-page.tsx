import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { SkontoPanel } from "./paper-form"

export function SkontoDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-cash-discount="desk">
      <CatalogHeading
        title="Skonto"
        subtitle="F2 cash_discount · kind + source_ref · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SkontoPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
