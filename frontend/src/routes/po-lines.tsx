import { createFileRoute } from "@tanstack/react-router"
import { PoLineDesk } from "@/features/po-line/catalog-page"

export const Route = createFileRoute("/po-lines")({
  component: PoLineDesk,
})
