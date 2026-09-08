import { createFileRoute } from "@tanstack/react-router"
import { DocumentTemplateBoard } from "@/features/document-template/catalog-page"

export const Route = createFileRoute("/document-templates")({
  component: DocumentTemplateBoard,
})
