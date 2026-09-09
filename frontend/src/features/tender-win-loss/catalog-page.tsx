import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { VerdictPanel } from "./verdict-form"

export function VerdictDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-win-loss="desk">
      <CatalogHeading
        title="Wynik przetargu"
        subtitle="G2.7 tender_win_loss · wynik + source_ref · nie extract RFP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <VerdictPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
