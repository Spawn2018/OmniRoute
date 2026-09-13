import { useQuery } from "@tanstack/react-query"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { loadOogPermitMarks } from "@/lib/oog-permit-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { OogPermitMarkSave } from "./mark-form"

export function OogPermitMarkDesk() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const ready = Boolean(organizationId && tenant.userId)
  const board = useQuery({
    enabled: ready,
    queryFn: loadOogPermitMarks,
    queryKey: ["oog-permit-board", organizationId],
    retry: false,
  })
  const permits = board.data ?? []

  return (
    <article className="space-y-6" data-oog-permit-mark="desk">
      <CatalogHeading
        title="Zezwolenie OOG"
        subtitle="BR4.1 oog_permit_mark · katalog HITL · nie wymiary Decimal · nie live urząd"
      />
      {ready ? null : <TenantSessionNotice />}
      {ready ? <OogPermitMarkSave organizationId={organizationId} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {ready && board.error == null ? (
        <dl className="max-w-2xl space-y-4" data-oog-permit-mark="catalog">
          {permits.map((permit) => (
            <div key={permit.id}>
              <dt className="font-mono text-sm">{permit.mark_code}</dt>
              <dd className="text-sm">Zezwolenie: {permit.permit_kind}</dd>
              <dd className="font-mono text-xs text-muted-foreground">{permit.source_ref}</dd>
            </div>
          ))}
        </dl>
      ) : null}
    </article>
  )
}
