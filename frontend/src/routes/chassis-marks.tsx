import { createFileRoute } from "@tanstack/react-router"
import { ChassisMarkBoard } from "@/features/chassis-mark/catalog-page"

export const Route = createFileRoute("/chassis-marks")({
  component: ChassisMarkBoard,
})
