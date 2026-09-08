import { createFileRoute } from "@tanstack/react-router"
import { OceanBillBoard } from "@/features/ocean-bill/catalog-page"

export const Route = createFileRoute("/ocean-bills")({
  component: OceanBillBoard,
})
