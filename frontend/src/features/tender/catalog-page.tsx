import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { SidePanel } from "./side-form"

export function BoardDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-tender="desk">
      <CatalogHeading
        title="Przetargi"
        subtitle="G2.0 tender · nagłówek sell/buy · nie auto-award"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SidePanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
