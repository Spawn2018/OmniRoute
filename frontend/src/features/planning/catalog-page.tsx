import { lazy, Suspense, useState } from "react"
import {
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"

const TripOverlay = lazy(() => import("@/features/planning/map-panel"))

function OverlayGate() {
  const [loadChunk, setLoadChunk] = useState(false)
  return (
    <details
      className="rounded-md border border-border bg-card p-3"
      data-planning="gate"
      onToggle={(event) => {
        if (event.currentTarget.open) setLoadChunk(true)
      }}
    >
      <summary className="cursor-pointer text-sm">Pokaż overlay przejazdów</summary>
      {loadChunk ? (
        <Suspense fallback={<p className="text-sm">Wciągam chunk mapy</p>}>
          <TripOverlay />
        </Suspense>
      ) : null}
    </details>
  )
}

export function PlanningBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  return (
    <section className="flex flex-col gap-4" data-planning="board">
      <CatalogHeading
        title="Planowanie"
        subtitle="T6 mapa · etykiety trip · chunk poza 250 kB · nie kafelki"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <OverlayGate /> : null}
    </section>
  )
}
