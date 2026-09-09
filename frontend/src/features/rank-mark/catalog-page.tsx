import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { RankWorkbench } from "./rank-workbench"

export function RankDesk() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const canWrite = orgId !== null && tenant.userId !== null
  return (
    <article className="flex flex-col gap-3" data-rank-mark="desk">
      <CatalogHeading
        title="Oś rankingu"
        subtitle="W5 rank_mark · oś zakupu · nie auto-award"
      />
      {canWrite ? <RankWorkbench organizationId={orgId} /> : <TenantSessionNotice />}
    </article>
  )
}
