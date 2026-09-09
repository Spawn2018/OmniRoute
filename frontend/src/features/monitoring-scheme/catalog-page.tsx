import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { SchemePanel } from "./scheme-form"

export function SchemeDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-monitoring-scheme="desk">
      <CatalogHeading
        title="Schemat monitoringu"
        subtitle="C7 monitoring_scheme · kod + source_ref · nie SENT XML"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SchemePanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
