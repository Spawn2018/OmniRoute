import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listFleetCostMarks, type FleetCostMarkRow } from "@/lib/fleet-cost-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FleetCostEntry } from "./mark-form"

const helper = createColumnHelper<FleetCostMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("cost_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function FleetCostDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const ready = Boolean(org && tenant.userId)
  const board = useQuery({
    enabled: ready,
    queryFn: listFleetCostMarks,
    queryKey: ["fleet-cost-marks", org],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-fleet="desk">
      <CatalogHeading
        title="Fleet cost"
        subtitle="EXP2.15 · katalog HITL · tco/maintenance/lease · bez silnika TCO"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <FleetCostEntry organizationId={org} /> : null}
      {board.error ? <CatalogError error={board.error} /> : null}
      {ready && board.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            cost_kind: "Rodzaj",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={board.data ?? []}
          globalFilterPlaceholder="Szukaj kosztów floty…"
          tableKey={BUSINESS_LISTS.fleetCostMark.tableKey}
        />
      ) : null}
    </section>
  )
}
