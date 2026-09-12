import { createFileRoute } from "@tanstack/react-router"
import { ImpersonateGuardMarkBoard } from "@/features/impersonate-guard-mark/catalog-page"

export const Route = createFileRoute("/impersonate-guard-marks")({
  component: ImpersonateGuardMarkBoard,
})
