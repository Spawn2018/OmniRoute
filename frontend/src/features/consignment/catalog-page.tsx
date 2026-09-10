import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { ParcelMarkPanel } from "./parcel-panel"

export function ConsignmentBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-consignment="board">
      <CatalogHeading
        title="Przesyłki"
        subtitle="N1 consignment · na zleceniu · nie paczka · nie FTL unique"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ParcelMarkPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
