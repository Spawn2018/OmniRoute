import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { RoundPanel } from "./round-form"

export function RoundDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender-round="desk">
      <CatalogHeading
        title="Rundy przetargu"
        subtitle="G2.3 tender_round · numer rundy · nie data room"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <RoundPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
