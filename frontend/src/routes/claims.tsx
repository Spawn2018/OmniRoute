import { createFileRoute } from "@tanstack/react-router"
import { CargoClaimPage } from "@/features/cargo-claim/catalog-page"

export const Route = createFileRoute("/claims")({
  component: CargoClaimPage,
})
