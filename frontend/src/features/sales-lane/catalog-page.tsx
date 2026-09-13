import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchSalesLanes, type SalesLaneRow } from "@/lib/sales-lanes-api"
import { getTenantContext } from "@/lib/tenant"
import { SalesLaneSave } from "./mark-form"

const helper = createColumnHelper<SalesLaneRow>()

const COLUMNS = [
  helper.accessor("lane_code", { header: "Kod" }),
  helper.accessor("lane_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function SalesLaneDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchSalesLanes,
    queryKey: ["sales-lanes", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-sales-lane="board">
      <CatalogHeading
        title="Korytarz sprzedażowy"
        subtitle="BR6.1 sales_lane · katalog HITL · nie UN/LOCODE · nie pipeline"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SalesLaneSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            lane_code: "Kod",
            lane_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj korytarza…"
          tableKey={BUSINESS_LISTS.salesLane.tableKey}
        />
      ) : null}
    </section>
  )
}
