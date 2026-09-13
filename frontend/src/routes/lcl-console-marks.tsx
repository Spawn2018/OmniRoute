import { createFileRoute } from "@tanstack/react-router"
import { LclConsoleMarkDesk } from "@/features/lcl-console-mark/catalog-page"

export const Route = createFileRoute("/lcl-console-marks")({
  component: LclConsoleMarkDesk,
})
