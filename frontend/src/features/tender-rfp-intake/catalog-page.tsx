import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { IntakePanel } from "./intake-form"

export function IntakeDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-rfp-intake="desk">
      <CatalogHeading
        title="Przyjęcie RFP"
        subtitle="G2.9 tender_rfp_intake · HITL + source_ref · nie zapis z LLM"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <IntakePanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
