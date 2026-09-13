import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCrmOpportunities, type CrmOpportunityRow } from "@/lib/crm-opportunities-api"
import { getTenantContext } from "@/lib/tenant"
import { CrmOpportunitySave } from "./mark-form"

const helper = createColumnHelper<CrmOpportunityRow>()

const COLUMNS = [
  helper.accessor("opportunity_code", { header: "Kod" }),
  helper.accessor("stage_kind", { header: "Etap" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CrmOpportunityDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCrmOpportunities,
    queryKey: ["crm-opportunities", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-crm-opportunity="board">
      <CatalogHeading
        title="Okazja CRM"
        subtitle="BR6.0 crm_opportunity · katalog HITL · nie pipeline · nie activity"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CrmOpportunitySave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            opportunity_code: "Kod",
            stage_kind: "Etap",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj okazji CRM…"
          tableKey={BUSINESS_LISTS.crmOpportunity.tableKey}
        />
      ) : null}
    </section>
  )
}
