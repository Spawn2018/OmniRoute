import { createFileRoute } from "@tanstack/react-router"
import { CellDesk } from "@/features/tender-matrix-cell/catalog-page"

export const Route = createFileRoute("/tender-matrix-cells")({
  component: CellDesk,
})
