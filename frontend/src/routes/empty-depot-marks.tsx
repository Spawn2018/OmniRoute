import { createFileRoute } from "@tanstack/react-router"
import { EmptyDepotMarkBoard } from "@/features/empty-depot-mark/catalog-page"

export const Route = createFileRoute("/empty-depot-marks")({
  component: EmptyDepotMarkBoard,
})
