import { createFileRoute } from "@tanstack/react-router"
import { CapaMarkDesk } from "@/features/capa-mark/catalog-page"

export const Route = createFileRoute("/capa-marks")({
  component: CapaMarkDesk,
})
