import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { PlayPanel } from "./play-form"

export function PlayDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-playbook="desk">
      <CatalogHeading
        title="Playbook przetargu"
        subtitle="G2.6 tender_playbook · twierdzenie + source_ref · nie extract RFP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PlayPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
