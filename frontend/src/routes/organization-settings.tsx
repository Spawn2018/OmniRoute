import { createFileRoute } from "@tanstack/react-router"
import { OrganizationSettingCatalogPage } from "@/features/organization-settings/catalog-page"

export const Route = createFileRoute("/organization-settings")({
  component: OrganizationSettingCatalogPage,
})
