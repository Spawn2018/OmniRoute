import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchEnforcementModes,
  type RoutingGuideEnforcementRow,
} from "@/lib/routing-guide-enforcements-api"
import { getTenantContext } from "@/lib/tenant"
import { EnforcementModeComposer } from "./enforcement-mode-composer"

const helper = createColumnHelper<RoutingGuideEnforcementRow>()
const TABLE_COLS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("enforcement_kind", { header: "Tryb" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function EnforcementModeDesk() {
  const session = getTenantContext()
  const tenantKey = session.organizationId
  const ready = Boolean(tenantKey && session.userId)
  const listing = useQuery({
    enabled: ready,
    queryFn: fetchEnforcementModes,
    queryKey: ["routing-guide-enforcements", tenantKey],
    retry: false,
  })
  return (
    <div className="space-y-8" data-enforcement-mode="desk">
      <CatalogHeading
        title="Egzekucja przewodnika"
        subtitle="CT4 leftover routing_guide_enforcement · katalog HITL · nie żywy 409"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <EnforcementModeComposer tenantKey={tenantKey} /> : null}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {ready && !listing.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            enforcement_kind: "Tryb",
            source_ref: "Pochodzenie",
          }}
          columns={TABLE_COLS}
          data={listing.data ?? []}
          globalFilterPlaceholder="Szukaj trybu…"
          tableKey={BUSINESS_LISTS.routingGuideEnforcement.tableKey}
        />
      ) : null}
    </div>
  )
}
