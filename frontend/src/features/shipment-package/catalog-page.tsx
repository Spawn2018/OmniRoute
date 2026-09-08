import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { ParcelScanPanel } from "./scan-panel"

export function ParcelDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-3" data-parcel="desk">
      <CatalogHeading
        title="Paczki na zleceniu"
        subtitle="D2 shipment_package · skan QR Omni · stop trasy · nie WMS"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ParcelScanPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
