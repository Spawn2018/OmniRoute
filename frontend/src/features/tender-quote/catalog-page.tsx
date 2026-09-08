import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { CapPanel } from "./cap-form"

export function BidDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-quote="desk">
      <CatalogHeading
        title="Oferty przetargowe kupna"
        subtitle="P6 tender_quote · ważność + limit orderów · nie auto-award"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CapPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
