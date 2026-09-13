import { createFileRoute } from "@tanstack/react-router"
import { VersionWindowBoard } from "@/features/version-window/catalog-page"

export const Route = createFileRoute("/version-windows")({
  component: VersionWindowBoard,
})
