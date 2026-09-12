import { createFileRoute } from "@tanstack/react-router"
import { CsrdMarkBoard } from "@/features/csrd-mark/catalog-page"

export const Route = createFileRoute("/csrd-marks")({
  component: CsrdMarkBoard,
})
