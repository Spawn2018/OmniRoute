import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { OpsIndex } from "@/features/ops/ops-index-page"
import { fetchHealth } from "@/lib/api"

export const Route = createFileRoute("/")({
  component: HomePage,
})

function HomePage() {
  const health = useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
    retry: false,
  })
  const healthState = health.isError ? "down" : health.data ? "ok" : "loading"
  const healthLabel = health.isError
    ? "niedostępne"
    : health.data
      ? health.data.status
      : "…"

  return <OpsIndex healthLabel={healthLabel} healthState={healthState} />
}
