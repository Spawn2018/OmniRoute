import { createFileRoute } from "@tanstack/react-router"
import { CreateBlockMarkDesk } from "@/features/create-block-mark/catalog-page"

export const Route = createFileRoute("/create-block-marks")({
  component: CreateBlockMarkDesk,
})
