import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { LevyKindPanel } from "./levy-form"

export function LocalDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-local-charge="desk">
      <CatalogHeading
        title="Dopłaty lokalne"
        subtitle="P4 local_charge · THC/ISPS + port + typ ISO · nie warning braków"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <LevyKindPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
