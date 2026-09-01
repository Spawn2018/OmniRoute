import { createFileRoute } from "@tanstack/react-router"
import { TerminalCatalogPage } from "@/features/geography/terminals-page"

export const Route = createFileRoute("/terminals")({
  component: TerminalCatalogPage,
})
