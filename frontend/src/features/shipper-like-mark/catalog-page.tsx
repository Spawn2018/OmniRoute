import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchShipperLikeMarks, type ShipperLikeMarkRow } from "@/lib/shipper-like-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ShipperLikeMarkSave } from "./mark-form"

const helper = createColumnHelper<ShipperLikeMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("like_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function ShipperLikeMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchShipperLikeMarks,
    queryKey: ["shipper-like-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-shipper-like-mark="board">
      <CatalogHeading
        title="Like-for-like załadowcy"
        subtitle="BR6.2 leftover shipper_like_mark · katalog HITL · nie Alpega · nie SQL"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ShipperLikeMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.shipperLikeMark.tableKey}
          globalFilterPlaceholder="Szukaj stance…"
          columns={COLUMNS}
          columnLabels={{
            mark_code: "Kod",
            like_kind: "Stance",
            source_ref: "Pochodzenie",
          }}
          data={listed.data ?? []}
        />
      ) : null}
    </section>
  )
}
