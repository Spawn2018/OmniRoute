import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchWmsFlowMarks, type WmsFlowMarkRow } from "@/lib/wms-flow-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { WmsFlowMarkSave } from "./mark-form"

const helper = createColumnHelper<WmsFlowMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("flow_kind", { header: "Przepływ" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function WmsFlowMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchWmsFlowMarks,
    queryKey: ["wms-flow-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-wms-flow-mark="board">
      <CatalogHeading
        title="Przepływ WMS"
        subtitle="BR1.0 wms_flow_mark · katalog HITL · nie live WMS · nie qty"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <WmsFlowMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            flow_kind: "Przepływ",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj operacji WMS…"
          tableKey={BUSINESS_LISTS.wmsFlowMark.tableKey}
        />
      ) : null}
    </section>
  )
}
