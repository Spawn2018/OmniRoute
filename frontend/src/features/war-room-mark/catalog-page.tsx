import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { RoomPanel } from "./room-form"

export function RoomDesk() {
  const session = getTenantContext()
  const orgId = session.organizationId
  if (!orgId || !session.userId) {
    return (
      <section className="grid gap-4" data-war-room="desk">
        <CatalogHeading
          title="Sala kryzysowa"
          subtitle="W2 war_room_mark · rodzaj incydentu · nie drugi czat"
        />
        <TenantSessionNotice />
      </section>
    )
  }
  return (
    <section className="grid gap-4" data-war-room="desk">
      <CatalogHeading
        title="Sala kryzysowa"
        subtitle="W2 war_room_mark · rodzaj incydentu · nie drugi czat"
      />
      <RoomPanel organizationId={orgId} />
    </section>
  )
}
