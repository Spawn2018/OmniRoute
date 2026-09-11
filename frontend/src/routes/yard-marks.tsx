import { createFileRoute } from "@tanstack/react-router"
import { YardMarkDesk } from "@/features/yard-mark/catalog-page"

export const Route = createFileRoute("/yard-marks")({
  component: YardMarkDesk,
})
