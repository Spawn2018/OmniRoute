import { createFileRoute } from "@tanstack/react-router"
import { SessionPage } from "@/features/session/session-page"

export const Route = createFileRoute("/session")({
  component: SessionPage,
})
