import { createFileRoute } from "@tanstack/react-router"
import { ImpactScenarioDesk } from "@/features/impact-scenario/catalog-page"

export const Route = createFileRoute("/impact-scenarios")({
  component: ImpactScenarioDesk,
})
