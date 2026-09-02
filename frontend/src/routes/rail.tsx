import { createFileRoute } from "@tanstack/react-router"
import { IntermodalRailPage } from "@/features/intermodal-rail/catalog-page"

export const Route = createFileRoute("/rail")({
  component: IntermodalRailPage,
})
