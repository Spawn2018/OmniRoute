import { createFileRoute } from "@tanstack/react-router"
import { BlocksCreateEnforcementMarkDesk } from "@/features/blocks-create-enforcement-mark/catalog-page"

export const Route = createFileRoute("/blocks-create-enforcement-marks")({
  component: BlocksCreateEnforcementMarkDesk,
})
