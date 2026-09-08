import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { DockWindowForm } from "./window-form"

export function DockDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-dock="desk">
      <CatalogHeading
        title="Awizacje doku"
        subtitle="D3 dock_appointment · okno na stop magazynu · nie WMS · nie T8"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <DockWindowForm organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
