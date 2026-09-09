import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { AwardReviewPanel } from "./review-form"

export function AwardReviewDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-award-review="desk">
      <CatalogHeading
        title="Cztery oczy nagrody"
        subtitle="G2.12 tender_award_review · countersign/challenge + source_ref · nie auto-award"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <AwardReviewPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
