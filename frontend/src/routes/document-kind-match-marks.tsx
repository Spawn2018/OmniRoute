import { createFileRoute } from "@tanstack/react-router"
import { DocumentKindMatchMarkDesk } from "@/features/document-kind-match-mark/catalog-page"

export const Route = createFileRoute("/document-kind-match-marks")({
  component: DocumentKindMatchMarkDesk,
})
