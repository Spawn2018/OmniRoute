import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchShipperTenderMarks, type ShipperTenderMarkRow } from "@/lib/shipper-tender-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ShipperTenderMarkSave } from "./mark-form"

const helper = createColumnHelper<ShipperTenderMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("shipper_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function ShipperTenderMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchShipperTenderMarks,
    queryKey: ["shipper-tender-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-shipper-tender-mark="board">
      <CatalogHeading
        title="Przetarg załadowcy"
        subtitle="BR6.2 shipper_tender_mark · katalog HITL · nie druga tabela tender · nie auto-award"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ShipperTenderMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            shipper_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj trybu…"
          tableKey={BUSINESS_LISTS.shipperTenderMark.tableKey}
        />
      ) : null}
    </section>
  )
}
