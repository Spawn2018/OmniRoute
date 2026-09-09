import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { PatternPanel } from "./pattern-form"

export function PatternDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-lane-pattern="desk">
      <CatalogHeading
        title="Wzorzec korytarza"
        subtitle="G2.19 lane_pattern · para UN/LOCODE + source_ref · nie circle_sim"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PatternPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
