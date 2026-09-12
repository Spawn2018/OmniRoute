import { createFileRoute } from "@tanstack/react-router"
import { WebhookOutboxBoard } from "@/features/webhook-outbox-mark/catalog-page"

export const Route = createFileRoute("/webhook-outbox-marks")({
  component: WebhookOutboxBoard,
})
