import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { RoomPanel } from "./room-form"

export function RoomDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-data-room="desk">
      <CatalogHeading
        title="Pokoje danych"
        subtitle="G2.4 tender_data_room · NDA jako dana · nie extract"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <RoomPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
