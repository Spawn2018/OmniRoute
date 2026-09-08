import { createFileRoute } from "@tanstack/react-router"
import { LocalDesk } from "@/features/local-charge/catalog-page"

export const Route = createFileRoute("/local-charges")({
  component: LocalDesk,
})
