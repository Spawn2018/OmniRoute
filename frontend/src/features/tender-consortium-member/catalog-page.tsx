import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { SeatPanel } from "./seat-form"

export function SeatDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-consortium-member="desk">
      <CatalogHeading
        title="Konsorcjum przetargu"
        subtitle="G2.8 tender_consortium_member · fotel + source_ref · nie extract RFP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SeatPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
