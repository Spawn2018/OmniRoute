import { createFileRoute } from "@tanstack/react-router"
import { GroupagePage } from "@/features/groupage/catalog-page"

export const Route = createFileRoute("/groupage")({
  component: GroupagePage,
})
