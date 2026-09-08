import { createFileRoute } from "@tanstack/react-router"
import { DockDesk } from "@/features/dock-appointment/catalog-page"

export const Route = createFileRoute("/dock-appointments")({
  component: DockDesk,
})
