import { createFileRoute } from "@tanstack/react-router"
import { KreptdDesk } from "@/features/kreptd-licence/catalog-page"

export const Route = createFileRoute("/kreptd-licences")({
  component: KreptdDesk,
})
