import { createFileRoute } from "@tanstack/react-router"
import { RagSopMarkBoard } from "@/features/rag-sop-mark/catalog-page"

export const Route = createFileRoute("/rag-sop-marks")({
  component: RagSopMarkBoard,
})
