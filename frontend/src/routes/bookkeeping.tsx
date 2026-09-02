import { createFileRoute } from "@tanstack/react-router"
import { BookkeepingPage } from "@/features/bookkeeping/catalog-page"

export const Route = createFileRoute("/bookkeeping")({
  component: BookkeepingPage,
})
