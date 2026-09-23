import { createFileRoute } from "@tanstack/react-router"
import { NetworkPrintGateMarkDesk } from "@/features/network-print-gate-mark/catalog-page"

export const Route = createFileRoute("/network-print-gate-marks")({
  component: NetworkPrintGateMarkDesk,
})
