import { createFileRoute } from "@tanstack/react-router"
import { SidImportBoard } from "@/features/sid-import-mark/catalog-page"

export const Route = createFileRoute("/sid-import-marks")({
  component: SidImportBoard,
})
