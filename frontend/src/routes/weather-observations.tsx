import { createFileRoute } from "@tanstack/react-router"
import { WeatherDesk } from "@/features/weather-observation/catalog-page"

export const Route = createFileRoute("/weather-observations")({
  component: WeatherDesk,
})
