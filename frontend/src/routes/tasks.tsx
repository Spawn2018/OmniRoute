import { createFileRoute } from "@tanstack/react-router"
import { TaskDesk } from "@/features/task/catalog-page"

export const Route = createFileRoute("/tasks")({
  component: TaskDesk,
})
