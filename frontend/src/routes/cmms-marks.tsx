import { createFileRoute } from "@tanstack/react-router"
import { CmmsMarkDesk } from "@/features/cmms-mark/catalog-page"

export const Route = createFileRoute("/cmms-marks")({
  component: CmmsMarkDesk,
})
