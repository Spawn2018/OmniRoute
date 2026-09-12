import { createFileRoute } from "@tanstack/react-router"
import { HubProtocolBoard } from "@/features/integration-hub-mark/catalog-page"

export const Route = createFileRoute("/integration-hub-marks")({
  component: HubProtocolBoard,
})
