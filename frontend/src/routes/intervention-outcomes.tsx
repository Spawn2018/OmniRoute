import { createFileRoute } from "@tanstack/react-router"
import { InterventionOutcomeDesk } from "@/features/intervention-outcome/catalog-page"

export const Route = createFileRoute("/intervention-outcomes")({
  component: InterventionOutcomeDesk,
})
