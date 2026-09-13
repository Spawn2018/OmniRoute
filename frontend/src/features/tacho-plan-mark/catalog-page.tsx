import { useQuery } from "@tanstack/react-query"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { loadTachoPlanMarks } from "@/lib/tacho-plan-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { TachoPlanMarkSave } from "./mark-form"

export function TachoPlanMarkDesk() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const deskOpen = Boolean(organizationId && tenant.userId)
  const listing = useQuery({
    enabled: deskOpen,
    queryFn: loadTachoPlanMarks,
    queryKey: ["tacho-plan-board", organizationId],
    retry: false,
  })
  const marks = listing.data ?? []

  return (
    <article className="space-y-6" data-tacho-plan-mark="desk">
      <CatalogHeading
        title="Tacho w planie"
        subtitle="BR3.3 tacho_plan_mark · katalog HITL · nie live DDD · nie solver godzin"
      />
      {deskOpen ? null : <TenantSessionNotice />}
      {deskOpen ? <TachoPlanMarkSave organizationId={organizationId} /> : null}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {deskOpen && listing.error == null ? (
        <ol className="max-w-2xl list-decimal space-y-3 pl-5" data-tacho-plan-mark="catalog">
          {marks.map((mark) => (
            <li key={mark.id}>
              <p className="font-mono text-sm">{mark.mark_code}</p>
              <p className="text-sm">Rodzaj: {mark.constraint_kind}</p>
              <p className="font-mono text-xs text-muted-foreground">{mark.source_ref}</p>
            </li>
          ))}
        </ol>
      ) : null}
    </article>
  )
}
