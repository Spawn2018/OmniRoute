import { createFileRoute } from "@tanstack/react-router"
import { RoomDesk } from "@/features/tender-data-room/catalog-page"

export const Route = createFileRoute("/tender-data-rooms")({
  component: RoomDesk,
})
