import { createFileRoute } from "@tanstack/react-router"
import { TelematicsDeviceDesk } from "@/features/telematics-device/catalog-page"

export const Route = createFileRoute("/telematics-devices")({
  component: TelematicsDeviceDesk,
})
