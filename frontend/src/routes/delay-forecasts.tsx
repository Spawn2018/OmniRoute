import { createFileRoute } from "@tanstack/react-router"
import { DelayForecastDesk } from "@/features/delay-forecast/catalog-page"

export const Route = createFileRoute("/delay-forecasts")({
  component: DelayForecastDesk,
})
