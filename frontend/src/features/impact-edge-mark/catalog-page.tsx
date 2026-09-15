import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchImpactEdgeMarks, type ImpactEdgeMarkRow } from "@/lib/impact-edge-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ImpactEdgeMarkSave } from "./mark-form"

const column = createColumnHelper<ImpactEdgeMarkRow>()

const TABLE_COLUMNS = [
  column.accessor("mark_code", { header: "Kod" }),
  column.accessor("from_kind", { header: "Od" }),
  column.accessor("to_kind", { header: "Do" }),
  column.accessor("source_ref", { header: "Pochodzenie" }),
]

export function ImpactEdgeMarkDesk() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const board = useQuery({
    enabled: sessionReady,
    queryFn: fetchImpactEdgeMarks,
    queryKey: ["impact-edge-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-impact-edge-mark="board">
      <CatalogHeading
        title="Krawedz skutku"
        subtitle="AI6.0 · HITL impact_edge_mark · para from/to · bez SQL grafu"
      />
      {!sessionReady ? <TenantSessionNotice /> : null}
      {sessionReady ? <ImpactEdgeMarkSave organizationId={organizationId} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {sessionReady && !board.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            from_kind: "Od",
            to_kind: "Do",
            source_ref: "Pochodzenie",
          }}
          columns={TABLE_COLUMNS}
          data={board.data ?? []}
          globalFilterPlaceholder="Filtruj krawedz skutku…"
          tableKey={BUSINESS_LISTS.impactEdgeMark.tableKey}
        />
      ) : null}
    </section>
  )
}
