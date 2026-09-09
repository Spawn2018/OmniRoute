import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { KreptdPanel } from "./licence-form"

export function KreptdDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-kreptd-licence="desk">
      <CatalogHeading
        title="Licencja KREPTD"
        subtitle="G2.23 kreptd_licence · numer licencji + source_ref · nie scrape"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <KreptdPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
