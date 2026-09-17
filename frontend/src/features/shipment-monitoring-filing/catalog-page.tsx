import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchShipmentMonitoringFilings,
  type ShipmentMonitoringFilingRow,
} from "@/lib/shipment-monitoring-filings-api"
import { getTenantContext } from "@/lib/tenant"
import { ShipmentMonitoringFilingSave } from "./mark-form"

const helper = createColumnHelper<ShipmentMonitoringFilingRow>()

const COLUMNS = [
  helper.accessor("filing_code", { header: "Kod" }),
  helper.accessor("status_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function ShipmentMonitoringFilingDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchShipmentMonitoringFilings,
    queryKey: ["shipment-monitoring-filings", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-shipment-monitoring-filing="board">
      <CatalogHeading
        title="Zgloszenie SENT/BDO"
        subtitle="C1 shipment_monitoring_filing · katalog HITL · nie live PUESC · nie XML SENT"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ShipmentMonitoringFilingSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            filing_code: "Kod",
            status_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj zgloszenia SENT/BDO…"
          tableKey={BUSINESS_LISTS.shipmentMonitoringFiling.tableKey}
        />
      ) : null}
    </section>
  )
}
