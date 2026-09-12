import { createFileRoute } from "@tanstack/react-router"
import { ErruMarkBoard } from "@/features/erru-mark/catalog-page"

export const Route = createFileRoute("/erru-marks")({
  component: ErruMarkBoard,
})
