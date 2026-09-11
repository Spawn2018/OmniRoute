import { createFileRoute } from "@tanstack/react-router"
import { OtifMarkDesk } from "@/features/otif-mark/catalog-page"

export const Route = createFileRoute("/otif-marks")({
  component: OtifMarkDesk,
})
