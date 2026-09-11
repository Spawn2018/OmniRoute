import { createFileRoute } from "@tanstack/react-router"
import { OogMarkDesk } from "@/features/oog-mark/catalog-page"

export const Route = createFileRoute("/oog-marks")({
  component: OogMarkDesk,
})
