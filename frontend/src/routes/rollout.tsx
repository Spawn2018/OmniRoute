import { createFileRoute } from "@tanstack/react-router"
import { TenantRolloutPage } from "@/features/tenant-rollout/catalog-page"

export const Route = createFileRoute("/rollout")({
  component: TenantRolloutPage,
})
