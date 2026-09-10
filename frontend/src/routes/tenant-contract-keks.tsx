import { createFileRoute } from "@tanstack/react-router"
import { TenantContractKekDesk } from "@/features/tenant-contract-kek/catalog-page"

export const Route = createFileRoute("/tenant-contract-keks")({
  component: TenantContractKekDesk,
})
