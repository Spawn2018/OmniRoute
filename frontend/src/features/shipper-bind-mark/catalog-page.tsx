import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchShipperBindMarks, type ShipperBindMarkRow } from "@/lib/shipper-bind-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ShipperBindMarkSave } from "./mark-form"

const helper = createColumnHelper<ShipperBindMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("bind_kind", { header: "Stance" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function ShipperBindMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchShipperBindMarks,
    queryKey: ["shipper-bind-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-shipper-bind-mark="panel">
      <CatalogHeading
        title="Bind załadowcy"
        subtitle="BR6.2 leftover shipper_bind_mark · katalog HITL · nie Alpega · nie FK UUID"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ShipperBindMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            bind_kind: "Stance",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtr bind załadowcy…"
          tableKey={BUSINESS_LISTS.shipperBindMark.tableKey}
        />
      ) : null}
    </section>
  )
}
