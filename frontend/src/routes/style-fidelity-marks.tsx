import { createFileRoute } from "@tanstack/react-router"
import { StyleFidelityMarkDesk } from "@/features/style-fidelity-mark/catalog-page"

export const Route = createFileRoute("/style-fidelity-marks")({
  component: StyleFidelityMarkDesk,
})
