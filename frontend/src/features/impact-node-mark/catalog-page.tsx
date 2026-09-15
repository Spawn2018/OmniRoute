import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchImpactNodeMarks, type ImpactNodeMarkRow } from "@/lib/impact-node-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ImpactNodeMarkSave } from "./mark-form"

const column = createColumnHelper<ImpactNodeMarkRow>()

const TABLE_COLUMNS = [
  column.accessor("mark_code", { header: "Kod" }),
  column.accessor("node_kind", { header: "Wezel" }),
  column.accessor("source_ref", { header: "Pochodzenie" }),
]

export function ImpactNodeMarkDesk() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const board = useQuery({
    enabled: sessionReady,
    queryFn: fetchImpactNodeMarks,
    queryKey: ["impact-node-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-impact-node-mark="board">
      <CatalogHeading
        title="Wezel skutku"
        subtitle="AI6.0 · HITL impact_node_mark · etykieta node_kind · bez SQL grafu"
      />
      {!sessionReady ? <TenantSessionNotice /> : null}
      {sessionReady ? <ImpactNodeMarkSave organizationId={organizationId} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {sessionReady && !board.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            node_kind: "Wezel",
            source_ref: "Pochodzenie",
          }}
          columns={TABLE_COLUMNS}
          data={board.data ?? []}
          globalFilterPlaceholder="Filtruj wezel skutku…"
          tableKey={BUSINESS_LISTS.impactNodeMark.tableKey}
        />
      ) : null}
    </section>
  )
}
