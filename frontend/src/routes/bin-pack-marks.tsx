import { createFileRoute } from "@tanstack/react-router"
import { BinPackDesk } from "@/features/bin-pack-mark/catalog-page"

export const Route = createFileRoute("/bin-pack-marks")({
  component: BinPackDesk,
})
