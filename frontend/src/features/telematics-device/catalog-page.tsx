import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchTelematicsDevices, type TelematicsDeviceRow } from "@/lib/telematics-devices-api"
import { getTenantContext } from "@/lib/tenant"
import { TelematicsDeviceSave } from "./mark-form"

const helper = createColumnHelper<TelematicsDeviceRow>()

const COLUMNS = [
  helper.accessor("device_code", { header: "Kod" }),
  helper.accessor("device_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function TelematicsDeviceDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchTelematicsDevices,
    queryKey: ["telematics-devices", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-telematics-device="board">
      <CatalogHeading
        title="Urządzenie telematyczne"
        subtitle="BR2.1 telematics_device · katalog HITL · nie parowanie · nie live poll"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <TelematicsDeviceSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            device_code: "Kod",
            device_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj urządzenia…"
          tableKey={BUSINESS_LISTS.telematicsDevice.tableKey}
        />
      ) : null}
    </section>
  )
}
