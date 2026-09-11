import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchLcChecklists, type LcChecklistRow } from "@/lib/lc-checklists-api"
import { getTenantContext } from "@/lib/tenant"
import { LcChecklistSave } from "./mark-form"

const helper = createColumnHelper<LcChecklistRow>()

const COLUMNS = [
  helper.accessor("checklist_code", { header: "Kod" }),
  helper.accessor("status_kind", { header: "Status" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function LcChecklistDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchLcChecklists,
    queryKey: ["lc-checklists", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-lc-checklist="board">
      <CatalogHeading
        title="Checklista LC"
        subtitle="G3 lc_checklist · katalog HITL · nie bank · nie due"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <LcChecklistSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            checklist_code: "Kod",
            status_kind: "Status",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj checklisty LC…"
          tableKey={BUSINESS_LISTS.lcChecklist.tableKey}
        />
      ) : null}
    </section>
  )
}
