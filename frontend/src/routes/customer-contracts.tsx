import { createFileRoute } from "@tanstack/react-router"
import { CustomerContractDesk } from "@/features/customer-contract/catalog-page"

export const Route = createFileRoute("/customer-contracts")({
  component: CustomerContractDesk,
})
