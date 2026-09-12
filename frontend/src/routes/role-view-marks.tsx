import { createFileRoute } from "@tanstack/react-router"
import { RoleViewMarkBoard } from "@/features/role-view-mark/catalog-page"

export const Route = createFileRoute("/role-view-marks")({
  component: RoleViewMarkBoard,
})
