import { createFileRoute } from "@tanstack/react-router"
import { MethodDesk } from "@/features/carbon-method/catalog-page"

export const Route = createFileRoute("/carbon-methods")({
  component: MethodDesk,
})
