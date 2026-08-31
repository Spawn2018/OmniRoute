import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
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

  return (
    <div className="space-y-3">
      <div>
        <h2 className="text-base font-semibold">Pulpit</h2>
        <p className="text-xs text-muted-foreground">
          Shell 0.5 · Vite · React Compiler · TanStack · shadcn tokens
        </p>
      </div>
      <div className="rounded-md border border-border bg-card p-3 text-sm">
        <div className="text-xs text-muted-foreground">API /health</div>
        {health.isLoading ? <div>Sprawdzanie…</div> : null}
        {health.isError ? (
          <div className="text-destructive">API niedostępne (uruchom backend na :8000)</div>
        ) : null}
        {health.data ? <div className="font-medium">status: {health.data.status}</div> : null}
      </div>
    </div>
  )
}
