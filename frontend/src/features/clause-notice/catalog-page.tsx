import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchClauseNotices, type ClauseNoticeRow } from "@/lib/clause-notices-api"
import { getTenantContext } from "@/lib/tenant"
import { ClauseNoticeSave } from "./notice-form"

const helper = createColumnHelper<ClauseNoticeRow>()

const COLUMNS = [
  helper.accessor("notice_code", { header: "Kod" }),
  helper.accessor("clause_label", { header: "Klauzula" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function ClauseNoticeDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchClauseNotices,
    queryKey: ["clause-notices", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-clause-notice="board">
      <CatalogHeading
        title="Powiadomienie o klauzuli"
        subtitle="CI3 clause_notice · katalog HITL · nie 409 · nie auto-kara"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ClauseNoticeSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            notice_code: "Kod",
            clause_label: "Klauzula",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj powiadomień…"
          tableKey={BUSINESS_LISTS.clauseNotice.tableKey}
        />
      ) : null}
    </section>
  )
}
