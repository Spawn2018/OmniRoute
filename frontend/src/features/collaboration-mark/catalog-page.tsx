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
  listCollaborationMarks,
  type CollaborationMarkRow,
} from "@/lib/collaboration-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CollaborationMarkWriter } from "./collaboration-mark-form"

const cols = createColumnHelper<CollaborationMarkRow>()
const COLUMNS = [
  cols.accessor("mark_code", { header: "Kod" }),
  cols.accessor("role_kind", { header: "Rola" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CollaborationMarkBoard() {
  const session = getTenantContext()
  const org = session.organizationId
  const online = Boolean(org && session.userId)
  const query = useQuery({
    enabled: online,
    queryFn: listCollaborationMarks,
    queryKey: ["collaboration-marks", org],
    retry: false,
  })
  return (
    <div className="space-y-6" data-collaboration-mark="board">
      <CatalogHeading
        title="Współpraca 3 stron"
        subtitle="CT11 collaboration_mark · katalog HITL · nie wspólny SELECT"
      />
      {!online ? <TenantSessionNotice /> : null}
      {online ? <CollaborationMarkWriter organizationId={org} /> : null}
      {query.error ? <CatalogError error={query.error} /> : null}
      {online && !query.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            role_kind: "Rola",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={query.data ?? []}
          globalFilterPlaceholder="Szukaj roli…"
          tableKey={BUSINESS_LISTS.collaborationMark.tableKey}
        />
      ) : null}
    </div>
  )
}
