import { createFileRoute } from "@tanstack/react-router"
import { SeatDesk } from "@/features/tender-consortium-member/catalog-page"

export const Route = createFileRoute("/tender-consortium-members")({
  component: SeatDesk,
})
