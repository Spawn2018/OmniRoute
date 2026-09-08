import { createFileRoute } from "@tanstack/react-router"
import { RoundDesk } from "@/features/tender-round/catalog-page"

export const Route = createFileRoute("/tender-rounds")({
  component: RoundDesk,
})
