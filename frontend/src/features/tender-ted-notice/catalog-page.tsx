import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { TedPanel } from "./notice-form"

export function TedDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-ted-notice="desk">
      <CatalogHeading
        title="Ogłoszenie TED"
        subtitle="G2.13 tender_ted_notice · numer TED + source_ref · nie scrape"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <TedPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
