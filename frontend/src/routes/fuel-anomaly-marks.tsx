import { createFileRoute } from "@tanstack/react-router"
import { FuelAnomalyCatalog } from "@/features/fuel-anomaly-mark/catalog-page"

export const Route = createFileRoute("/fuel-anomaly-marks")({
  component: FuelAnomalyCatalog,
})
