import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchShipperAwardMarks, type ShipperAwardMarkRow } from "@/lib/shipper-award-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ShipperAwardMarkSave } from "./mark-form"

const awardHelper = createColumnHelper<ShipperAwardMarkRow>()

const AWARD_TABLE = [
  awardHelper.accessor("mark_code", { header: "Kod award" }),
  awardHelper.accessor("award_kind", { header: "Decyzja" }),
  awardHelper.accessor("source_ref", { header: "Źródło" }),
]

export function ShipperAwardMarkDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const canLoad = Boolean(org && tenant.userId)
  const query = useQuery({
    enabled: canLoad,
    queryFn: fetchShipperAwardMarks,
    queryKey: ["shipper-award-marks", org],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-shipper-award-mark="desk">
      <CatalogHeading
        title="Award załadowcy"
        subtitle="BR6.2 shipper_award_mark · HITL · nie Alpega · nie auto-award SQL"
      />
      {canLoad ? null : <TenantSessionNotice />}
      {canLoad ? <ShipperAwardMarkSave organizationId={org} /> : null}
      {query.error ? <CatalogError error={query.error} /> : null}
      {canLoad && query.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod award",
            award_kind: "Decyzja",
            source_ref: "Źródło",
          }}
          columns={AWARD_TABLE}
          data={query.data ?? []}
          globalFilterPlaceholder="Filtr award…"
          tableKey={BUSINESS_LISTS.shipperAwardMark.tableKey}
        />
      ) : null}
    </section>
  )
}
