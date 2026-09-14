import { createFileRoute } from "@tanstack/react-router"
import { WmsFlowMarkDesk } from "@/features/wms-flow-mark/catalog-page"

export const Route = createFileRoute("/wms-flow-marks")({
  component: WmsFlowMarkDesk,
})
