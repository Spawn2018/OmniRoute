import { createFileRoute } from "@tanstack/react-router"
import { MailAcceptMarkBoard } from "@/features/mail-accept-mark/catalog-page"

export const Route = createFileRoute("/mail-accept-marks")({
  component: MailAcceptMarkBoard,
})
