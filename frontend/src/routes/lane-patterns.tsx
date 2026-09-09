import { createFileRoute } from "@tanstack/react-router"
import { PatternDesk } from "@/features/lane-pattern/catalog-page"

export const Route = createFileRoute("/lane-patterns")({
  component: PatternDesk,
})
