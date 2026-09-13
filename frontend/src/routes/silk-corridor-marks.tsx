import { createFileRoute } from "@tanstack/react-router"
import { SilkCorridorMarkDesk } from "@/features/silk-corridor-mark/catalog-page"

export const Route = createFileRoute("/silk-corridor-marks")({
  component: SilkCorridorMarkDesk,
})
