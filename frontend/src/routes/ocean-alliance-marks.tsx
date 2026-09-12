import { createFileRoute } from "@tanstack/react-router"
import { OceanAllianceMarkBoard } from "@/features/ocean-alliance-mark/catalog-page"

export const Route = createFileRoute("/ocean-alliance-marks")({
  component: OceanAllianceMarkBoard,
})
