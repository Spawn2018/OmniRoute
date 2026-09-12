import { createFileRoute } from "@tanstack/react-router"
import { MobileClientMarkBoard } from "@/features/mobile-client-mark/catalog-page"

export const Route = createFileRoute("/mobile-client-marks")({
  component: MobileClientMarkBoard,
})
