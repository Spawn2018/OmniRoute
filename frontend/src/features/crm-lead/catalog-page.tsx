import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCrmLeads, type CrmLeadRow } from "@/lib/crm-leads-api"
import { getTenantContext } from "@/lib/tenant"
import { CrmLeadSave } from "./mark-form"

const helper = createColumnHelper<CrmLeadRow>()

const COLUMNS = [
  helper.accessor("lead_code", { header: "Kod" }),
  helper.accessor("stage_kind", { header: "Etap" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CrmLeadDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCrmLeads,
    queryKey: ["crm-leads", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-crm-lead="board">
      <CatalogHeading
        title="Lead CRM"
        subtitle="G1 crm_lead · katalog HITL · nie szansa · nie cold-send"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CrmLeadSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            lead_code: "Kod",
            stage_kind: "Etap",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj leada CRM…"
          tableKey={BUSINESS_LISTS.crmLead.tableKey}
        />
      ) : null}
    </section>
  )
}
