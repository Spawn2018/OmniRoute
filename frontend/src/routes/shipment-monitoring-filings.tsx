import { createFileRoute } from "@tanstack/react-router"
import { ShipmentMonitoringFilingDesk } from "@/features/shipment-monitoring-filing/catalog-page"

export const Route = createFileRoute("/shipment-monitoring-filings")({
  component: ShipmentMonitoringFilingDesk,
})
