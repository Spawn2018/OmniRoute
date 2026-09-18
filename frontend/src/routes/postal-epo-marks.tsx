import { createFileRoute } from "@tanstack/react-router"
import { PostalEpoMarkDesk } from "@/features/postal-epo-mark/catalog-page"

export const Route = createFileRoute("/postal-epo-marks")({
  component: PostalEpoMarkDesk,
})
