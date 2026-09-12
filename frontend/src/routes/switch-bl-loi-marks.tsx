import { createFileRoute } from "@tanstack/react-router"
import { SwitchBlLoiBoard } from "@/features/switch-bl-loi-mark/catalog-page"

export const Route = createFileRoute("/switch-bl-loi-marks")({
  component: SwitchBlLoiBoard,
})
