import { createFileRoute } from "@tanstack/react-router"
import { ClockDesk } from "@/features/free-time-clock/catalog-page"

export const Route = createFileRoute("/free-time-clocks")({
  component: ClockDesk,
})
