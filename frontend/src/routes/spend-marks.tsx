import { createFileRoute } from "@tanstack/react-router"
import { SpendMarkDesk } from "@/features/spend-mark/catalog-page"

export const Route = createFileRoute("/spend-marks")({
  component: SpendMarkDesk,
})
