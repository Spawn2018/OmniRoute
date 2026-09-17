import { createFileRoute } from "@tanstack/react-router"
import { PostalDispatchMarkDesk } from "@/features/postal-dispatch-mark/catalog-page"

export const Route = createFileRoute("/postal-dispatch-marks")({
  component: PostalDispatchMarkDesk,
})
