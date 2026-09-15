import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCrmLinkMarks, type CrmLinkMarkRow } from "@/lib/crm-link-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CrmLinkMarkSave } from "./mark-form"

const helper = createColumnHelper<CrmLinkMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("link_kind", { header: "Stance" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CrmLinkMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCrmLinkMarks,
    queryKey: ["crm-link-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-crm-link-mark="board">
      <CatalogHeading
        title="Link CRM"
        subtitle="BR6.0 leftover crm_link_mark · katalog HITL · nie FK UUID · nie cold-send"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CrmLinkMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            link_kind: "Powiązanie",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj powiązań CRM…"
          tableKey={BUSINESS_LISTS.crmLinkMark.tableKey}
        />
      ) : null}
    </section>
  )
}
