import { createFileRoute } from "@tanstack/react-router"
import { CargoCoverMarkDesk } from "@/features/cargo-cover-mark/catalog-page"

export const Route = createFileRoute("/cargo-cover-marks")({
  component: CargoCoverMarkDesk,
})
