import { createFileRoute } from "@tanstack/react-router"
import { Article50MarkDesk } from "@/features/article50-mark/catalog-page"

export const Route = createFileRoute("/article50-marks")({
  component: Article50MarkDesk,
})
