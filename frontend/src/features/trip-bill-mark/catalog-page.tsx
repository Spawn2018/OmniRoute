import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchTripBillMarks,
  type TripBillMarkRow,
} from "@/lib/trip-bill-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { TripBillMarkSave } from "./mark-form"

const helper = createColumnHelper<TripBillMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("bill_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function TripBillMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchTripBillMarks,
    queryKey: ["trip-bill-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-trip-bill-mark="board">
      <CatalogHeading
        title="Gotowość przejazdu do FV"
        subtitle="N2 trip_bill_mark · HITL ready/held/billed · nie SQL trips_to_bill"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <TripBillMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            bill_kind: "Rodzaj",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj znaczniki gotowości do FV…"
          tableKey={BUSINESS_LISTS.tripBillMark.tableKey}
        />
      ) : null}
    </section>
  )
}
