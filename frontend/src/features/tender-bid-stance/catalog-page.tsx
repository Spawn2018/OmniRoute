import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { StancePanel } from "./stance-form"

export function StanceDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-bid-stance="desk">
      <CatalogHeading
        title="Udział w przetargu"
        subtitle="G2.11 tender_bid_stance · bid/no-bid + source_ref · nie auto-award"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <StancePanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
