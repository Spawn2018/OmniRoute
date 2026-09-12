import { createFileRoute } from "@tanstack/react-router"
import { HaulierRoleMarkBoard } from "@/features/haulier-role-mark/catalog-page"

export const Route = createFileRoute("/haulier-role-marks")({
  component: HaulierRoleMarkBoard,
})
