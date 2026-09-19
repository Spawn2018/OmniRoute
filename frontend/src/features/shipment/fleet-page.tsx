import {
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { FleetResourcePanel } from "@/features/shipment/fleet-resource-panel"
import { ResourceDocumentPanel } from "@/features/shipment/resource-document-panel"
import { getTenantContext } from "@/lib/tenant"

export function FleetPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  return (
    <div className="flex flex-col gap-4" data-fleet="board">
      <CatalogHeading
        title="Flota"
        subtitle="resource T2 · pojazd / kierowca / naczepa · nie GPS"
      />
      {!ready ? <TenantSessionNotice /> : null}
      <FleetResourcePanel signedIn={ready} />
      <ResourceDocumentPanel signedIn={ready} />
    </div>
  )
}
