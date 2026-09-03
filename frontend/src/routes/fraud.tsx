import { createFileRoute } from "@tanstack/react-router"
import { FraudFlagPage } from "@/features/fraud-flag/catalog-page"

export const Route = createFileRoute("/fraud")({
  component: FraudFlagPage,
})
