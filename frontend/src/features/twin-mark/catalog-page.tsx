import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { TwinPanel } from "./twin-form"

export function TwinDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-twin-mark="desk">
      <CatalogHeading
        title="Bliźniak"
        subtitle="W1 twin_mark · osiem rodzajów · nie fizyka"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <TwinPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
