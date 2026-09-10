import { createFileRoute } from "@tanstack/react-router"
import { TerminalSlotConnectorDesk } from "@/features/terminal-slot-connector/catalog-page"

export const Route = createFileRoute("/terminal-slot-connectors")({
  component: TerminalSlotConnectorDesk,
})
