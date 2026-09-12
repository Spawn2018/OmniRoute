import { createFileRoute } from "@tanstack/react-router"
import { PhytoAtaBoard } from "@/features/phyto-ata-mark/catalog-page"

export const Route = createFileRoute("/phyto-ata-marks")({
  component: PhytoAtaBoard,
})
