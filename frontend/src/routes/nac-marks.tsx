import { createFileRoute } from "@tanstack/react-router"
import { NacMarkDesk } from "@/features/nac-mark/catalog-page"

export const Route = createFileRoute("/nac-marks")({
  component: NacMarkDesk,
})
