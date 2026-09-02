import { createFileRoute } from "@tanstack/react-router"
import { OperationalExceptionPage } from "@/features/operational-exception/catalog-page"

export const Route = createFileRoute("/exceptions")({
  component: OperationalExceptionPage,
})
