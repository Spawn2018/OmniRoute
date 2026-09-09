import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { ConnectorPanel } from "./connector-form"

export function ConnectorDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-telematics-connector="desk">
      <CatalogHeading
        title="Konektor GPS"
        subtitle="V5 telematics_connector · reżim + dostawca · nie live poll"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ConnectorPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
