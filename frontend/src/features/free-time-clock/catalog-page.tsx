import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { ClockPanel } from "./clock-form"

export function ClockDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-free-time-clock="desk">
      <CatalogHeading
        title="Zegar DD"
        subtitle="V3 free_time_clock · rodzaj + dni wolne · nie countdown"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ClockPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
