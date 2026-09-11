import { createFileRoute } from "@tanstack/react-router"
import { FerryArt9Screen } from "@/features/ferry-art9-mark/catalog-page"

export const Route = createFileRoute("/ferry-art9-marks")({
  component: FerryArt9Screen,
})
