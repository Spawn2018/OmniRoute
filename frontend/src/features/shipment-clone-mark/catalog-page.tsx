import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchShipmentCloneMarks,
  type ShipmentCloneMarkRow,
} from "@/lib/shipment-clone-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ShipmentCloneMarkSave } from "./mark-form"

const helper = createColumnHelper<ShipmentCloneMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("clone_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function ShipmentCloneMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchShipmentCloneMarks,
    queryKey: ["shipment-clone-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-shipment-clone-mark="board">
      <CatalogHeading
        title="Intencja klonu zlecenia"
        subtitle="N9 shipment_clone_mark · HITL last_similar/manual_pick · nie drugi SoR"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <ShipmentCloneMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            clone_kind: "Rodzaj",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj intencje klonu…"
          tableKey={BUSINESS_LISTS.shipmentCloneMark.tableKey}
        />
      ) : null}
    </section>
  )
}
