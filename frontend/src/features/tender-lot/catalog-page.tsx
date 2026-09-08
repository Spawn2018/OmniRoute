import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { LotPanel } from "./lot-form"

export function LotDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-lot="desk">
      <CatalogHeading
        title="Partie przetargu"
        subtitle="G2.1 tender_lot · kod partii · nie korytarz"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <LotPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
