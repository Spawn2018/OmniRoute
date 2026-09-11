import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  listSubcontractEdgeMarks,
  type SubcontractEdgeMarkRow,
} from "@/lib/subcontract-edge-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SubcontractEdgeMarkEditor } from "./mark-form"

const col = createColumnHelper<SubcontractEdgeMarkRow>()

const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("edge_kind", { header: "Krawędź" }),
  col.accessor("source_ref", { header: "Źródło" }),
]

export function SubcontractEdgeMarkDesk() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const list = useQuery({
    enabled: ready,
    queryFn: listSubcontractEdgeMarks,
    queryKey: ["subcontract-edge-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-subcontract-edge-mark="desk">
      <CatalogHeading
        title="Subcontract edge"
        subtitle="EXP2.6 · HITL subcontract_edge_mark · edge_kind · bez grafu live"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SubcontractEdgeMarkEditor organizationId={orgId} /> : null}
      {list.error ? <CatalogError error={list.error} /> : null}
      {ready && !list.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            edge_kind: "Krawędź",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={list.data ?? []}
          globalFilterPlaceholder="Filtruj edge…"
          tableKey={BUSINESS_LISTS.subcontractEdgeMark.tableKey}
        />
      ) : null}
    </section>
  )
}
