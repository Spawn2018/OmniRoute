import { createFileRoute } from "@tanstack/react-router"
import { BlueprintDesk } from "@/features/task-template/catalog-page"

export const Route = createFileRoute("/task-templates")({
  component: BlueprintDesk,
})
