import { createFileRoute } from "@tanstack/react-router"
import { StyleCascadeMarkDesk } from "@/features/style-cascade-mark/catalog-page"

export const Route = createFileRoute("/style-cascade-marks")({
  component: StyleCascadeMarkDesk,
})
