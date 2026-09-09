import { createFileRoute } from "@tanstack/react-router"
import { ImpactDesk } from "@/features/tower-impact/catalog-page"

export const Route = createFileRoute("/tower-impacts")({
  component: ImpactDesk,
})
