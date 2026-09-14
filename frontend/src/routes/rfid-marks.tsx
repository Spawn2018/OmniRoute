import { createFileRoute } from "@tanstack/react-router"
import { RfidMarkDesk } from "@/features/rfid-mark/catalog-page"

export const Route = createFileRoute("/rfid-marks")({
  component: RfidMarkDesk,
})
