import { createFileRoute } from "@tanstack/react-router"
import { RegistryPollMarkDesk } from "@/features/registry-poll-mark/catalog-page"

export const Route = createFileRoute("/registry-poll-marks")({
  component: RegistryPollMarkDesk,
})
