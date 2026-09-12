import { createFileRoute } from "@tanstack/react-router"
import { CopyBanMarkBoard } from "@/features/copy-ban-mark/catalog-page"

export const Route = createFileRoute("/copy-ban-marks")({
  component: CopyBanMarkBoard,
})
