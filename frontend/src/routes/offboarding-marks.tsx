import { createFileRoute } from "@tanstack/react-router"
import { OffboardingBoard } from "@/features/offboarding-mark/catalog-page"

export const Route = createFileRoute("/offboarding-marks")({
  component: OffboardingBoard,
})
