import { createFileRoute } from "@tanstack/react-router"
import { OpsRoomMarkDesk } from "@/features/ops-room-mark/catalog-page"

export const Route = createFileRoute("/ops-room-marks")({
  component: OpsRoomMarkDesk,
})
