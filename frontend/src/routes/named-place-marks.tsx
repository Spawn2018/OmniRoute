import { createFileRoute } from "@tanstack/react-router"
import { NamedPlaceMarkBoard } from "@/features/named-place-mark/catalog-page"

export const Route = createFileRoute("/named-place-marks")({
  component: NamedPlaceMarkBoard,
})
