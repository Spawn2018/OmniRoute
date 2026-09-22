import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { HouseKindPanel } from "./kind-panel"

export function OceanBillBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-ocean-bill="board">
      <CatalogHeading
        title="Konosament LCL"
        subtitle="D6 ocean_bill · HBL/MBL · pule M-03 · nie PDF · nie booking"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <HouseKindPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
