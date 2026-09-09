import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { ProspectPanel } from "./prospect-form"

export function ProspectDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-prospect="desk">
      <CatalogHeading
        title="Prospekt przetargu"
        subtitle="G2.10 tender_prospect · outreach + source_ref · nie scrape"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ProspectPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
