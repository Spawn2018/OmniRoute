import { createFileRoute } from "@tanstack/react-router"
import { OceanLclPage } from "@/features/ocean-lcl/catalog-page"

export const Route = createFileRoute("/lcl")({
  component: OceanLclPage,
})
