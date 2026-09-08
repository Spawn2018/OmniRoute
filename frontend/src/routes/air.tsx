import { createFileRoute } from "@tanstack/react-router"
import { AirPage } from "@/features/air-freight/catalog-page"

export const Route = createFileRoute("/air")({
  component: AirPage,
})
