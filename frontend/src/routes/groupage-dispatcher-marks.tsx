import { createFileRoute } from "@tanstack/react-router"
import { GroupageDispatcherMarkDesk } from "@/features/groupage-dispatcher-mark/catalog-page"

export const Route = createFileRoute("/groupage-dispatcher-marks")({
  component: GroupageDispatcherMarkDesk,
})
