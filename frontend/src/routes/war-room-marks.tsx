import { createFileRoute } from "@tanstack/react-router"
import { RoomDesk } from "@/features/war-room-mark/catalog-page"

export const Route = createFileRoute("/war-room-marks")({
  component: RoomDesk,
})
