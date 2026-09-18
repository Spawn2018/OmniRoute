import { createFileRoute } from "@tanstack/react-router"
import { WasteMarkDesk } from "@/features/waste-mark/catalog-page"

export const Route = createFileRoute("/waste-marks")({
  component: WasteMarkDesk,
})
