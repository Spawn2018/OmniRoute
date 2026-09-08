import { createFileRoute } from "@tanstack/react-router"
import { BoardDesk } from "@/features/tender/catalog-page"

export const Route = createFileRoute("/tenders")({
  component: BoardDesk,
})
