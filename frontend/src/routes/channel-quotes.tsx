import { createFileRoute } from "@tanstack/react-router"
import { ChannelQuoteCatalogPage } from "@/features/channel-quotes/catalog-page"

export const Route = createFileRoute("/channel-quotes")({
  component: ChannelQuoteCatalogPage,
})
