import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { LanePanel } from "./lane-form"

export function LaneDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-lane="desk">
      <CatalogHeading
        title="Korytarze przetargu"
        subtitle="G2.2 tender_lane · para UN/LOCODE · nie runda"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <LanePanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
