import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchShipperRoundMarks, type ShipperRoundMarkRow } from "@/lib/shipper-round-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ShipperRoundMarkSave } from "./mark-form"

const helper = createColumnHelper<ShipperRoundMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("round_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function ShipperRoundMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchShipperRoundMarks,
    queryKey: ["shipper-round-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-shipper-round-mark="board">
      <CatalogHeading
        title="Runda załadowcy"
        subtitle="BR6.2 leftover shipper_round_mark · katalog HITL · nie Alpega · nie like-for-like"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ShipperRoundMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            round_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj trybu…"
          tableKey={BUSINESS_LISTS.shipperRoundMark.tableKey}
        />
      ) : null}
    </section>
  )
}
