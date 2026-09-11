import { createFileRoute } from "@tanstack/react-router"
import { EnforcementModeDesk } from "@/features/routing-guide-enforcement/enforcement-mode-desk"

export const Route = createFileRoute("/routing-guide-enforcements")({
  component: EnforcementModeDesk,
})
