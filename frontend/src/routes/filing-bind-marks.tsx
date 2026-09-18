import { createFileRoute } from "@tanstack/react-router"
import { FilingBindMarkDesk } from "@/features/filing-bind-mark/catalog-page"

export const Route = createFileRoute("/filing-bind-marks")({
  component: FilingBindMarkDesk,
})
