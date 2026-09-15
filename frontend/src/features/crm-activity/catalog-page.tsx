import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCrmActivities, type CrmActivityRow } from "@/lib/crm-activities-api"
import { getTenantContext } from "@/lib/tenant"
import { CrmActivitySave } from "./mark-form"

const helper = createColumnHelper<CrmActivityRow>()

const COLUMNS = [
  helper.accessor("activity_code", { header: "Kod" }),
  helper.accessor("activity_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CrmActivityDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCrmActivities,
    queryKey: ["crm-activities", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-crm-activity="board">
      <CatalogHeading
        title="Aktywność CRM"
        subtitle="BR6.0 crm_activity · katalog HITL · nie pipeline · nie FK okazji"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CrmActivitySave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            activity_code: "Kod",
            activity_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj aktywności CRM…"
          tableKey={BUSINESS_LISTS.crmActivity.tableKey}
        />
      ) : null}
    </section>
  )
}
