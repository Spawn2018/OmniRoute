import { createFileRoute } from "@tanstack/react-router"
import { WhatIfMarkBoard } from "@/features/what-if-mark/catalog-page"

export const Route = createFileRoute("/what-if-marks")({
  component: WhatIfMarkBoard,
})
