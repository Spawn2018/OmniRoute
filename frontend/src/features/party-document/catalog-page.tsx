import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { PartyDocPanel } from "./paper-form"

export function PartyDocDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-party-document="desk">
      <CatalogHeading
        title="Dokument kontrahenta"
        subtitle="C8 party_document · kind + source_ref · nie 409"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PartyDocPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
