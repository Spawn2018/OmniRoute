import { createFileRoute } from "@tanstack/react-router"
import { CloneCarryMarkDesk } from "@/features/clone-carry-mark/catalog-page"

export const Route = createFileRoute("/clone-carry-marks")({
  component: CloneCarryMarkDesk,
})
