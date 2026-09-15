import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCrmDedupMarks, type CrmDedupMarkRow } from "@/lib/crm-dedup-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CrmDedupMarkSave } from "./mark-form"

const helper = createColumnHelper<CrmDedupMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("dedup_kind", { header: "Stance" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CrmDedupMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCrmDedupMarks,
    queryKey: ["crm-dedup-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-crm-dedup-mark="board">
      <CatalogHeading
        title="Dedup CRM"
        subtitle="BR6.0 leftover crm_dedup_mark · katalog HITL · nie merge SQL · nie cold-send"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CrmDedupMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.crmDedupMark.tableKey}
          globalFilterPlaceholder="Szukaj stance dedup…"
          columns={COLUMNS}
          columnLabels={{
            mark_code: "Kod",
            dedup_kind: "Stance",
            source_ref: "Pochodzenie",
          }}
          data={listed.data ?? []}
        />
      ) : null}
    </section>
  )
}
