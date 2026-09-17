import { createFileRoute } from "@tanstack/react-router"
import { InvoiceMatchCandidateDesk } from "@/features/invoice-match-candidate/catalog-page"

export const Route = createFileRoute("/invoice-match-candidates")({
  component: InvoiceMatchCandidateDesk,
})
