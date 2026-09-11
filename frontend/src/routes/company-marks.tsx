import { createFileRoute } from "@tanstack/react-router"
import { CompanyMarkDesk } from "@/features/company-mark/catalog-page"

export const Route = createFileRoute("/company-marks")({
  component: CompanyMarkDesk,
})
