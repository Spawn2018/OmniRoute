import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { BriefStage } from "./brief-stage"

export function BriefDesk() {
  const tenant = getTenantContext()
  const hasSession = Boolean(tenant.organizationId && tenant.userId)
  if (!hasSession) {
    return (
      <main className="flex flex-col gap-6" data-executive-mark="desk">
        <CatalogHeading
          title="Pytanie zarządu"
          subtitle="W4 executive_mark · rodzaj pytania · nie suma z modelu"
        />
        <TenantSessionNotice />
      </main>
    )
  }
  return (
    <main className="flex flex-col gap-6" data-executive-mark="desk">
      <CatalogHeading
        title="Pytanie zarządu"
        subtitle="W4 executive_mark · rodzaj pytania · nie suma z modelu"
      />
      <BriefStage organizationId={tenant.organizationId} />
    </main>
  )
}
