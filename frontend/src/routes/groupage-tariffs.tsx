import { createFileRoute } from "@tanstack/react-router"
import { TariffDesk } from "@/features/groupage-tariff/catalog-page"

export const Route = createFileRoute("/groupage-tariffs")({
  component: TariffDesk,
})
