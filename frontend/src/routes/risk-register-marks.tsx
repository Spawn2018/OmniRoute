import { createFileRoute } from "@tanstack/react-router"
import { RiskRegisterMarkDesk } from "@/features/risk-register-mark/catalog-page"

export const Route = createFileRoute("/risk-register-marks")({
  component: RiskRegisterMarkDesk,
})
