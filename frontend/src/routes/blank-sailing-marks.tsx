import { createFileRoute } from "@tanstack/react-router"
import { BlankSailingMarkDesk } from "@/features/blank-sailing-mark/catalog-page"

export const Route = createFileRoute("/blank-sailing-marks")({
  component: BlankSailingMarkDesk,
})
