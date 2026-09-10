import { createFileRoute } from "@tanstack/react-router"
import { CircleDesk } from "@/features/circle-sim/catalog-page"

export const Route = createFileRoute("/circle-sims")({
  component: CircleDesk,
})
