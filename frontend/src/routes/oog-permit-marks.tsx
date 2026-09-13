import { createFileRoute } from "@tanstack/react-router"
import { OogPermitMarkDesk } from "@/features/oog-permit-mark/catalog-page"

export const Route = createFileRoute("/oog-permit-marks")({
  component: OogPermitMarkDesk,
})
