import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { StopGroupPanel } from "./group-panel"

export function StopGroupBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-stop-group="board">
      <CatalogHeading
        title="Grupy punktów"
        subtitle="T1b stop_group · nagłówek na zleceniu · nie członkostwo · nie mapa"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <StopGroupPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
