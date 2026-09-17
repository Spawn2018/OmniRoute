import { createFileRoute } from "@tanstack/react-router"
import { RelationDocumentRequirementDesk } from "@/features/relation-document-requirement/catalog-page"

export const Route = createFileRoute("/relation-document-requirements")({
  component: RelationDocumentRequirementDesk,
})
