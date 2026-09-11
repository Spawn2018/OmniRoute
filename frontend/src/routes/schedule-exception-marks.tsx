import { createFileRoute } from "@tanstack/react-router"
import { ScheduleExceptionMarkDesk } from "@/features/schedule-exception-mark/catalog-page"

export const Route = createFileRoute("/schedule-exception-marks")({
  component: ScheduleExceptionMarkDesk,
})
