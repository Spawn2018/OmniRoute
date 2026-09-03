import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { createTrackingEvent, fetchTrackingEvents } from "@/lib/tracking-events-api"
import { getTenantContext } from "@/lib/tenant"

function TrackingEventForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [shipmentId, setShipmentId] = useState("")
  const [eventKind, setEventKind] = useState("departed")
  const [occurredAt, setOccurredAt] = useState("2026-09-03T10:00:00+00:00")
  const [sourceRef, setSourceRef] = useState("fixture://tracking/")
  const save = useMutation({
    mutationFn: () =>
      createTrackingEvent({
        shipment_id: shipmentId.trim(),
        event_kind: eventKind.trim(),
        occurred_at: occurredAt.trim(),
        source_ref: sourceRef.trim(),
      }),
    onSuccess: () => {
      setShipmentId("")
      void client.invalidateQueries({ queryKey: ["tracking-events", args.organizationId] })
    },
  })
  return (
    <form
      className="flex flex-wrap items-end gap-2 rounded-md border border-border bg-card p-3"
      onSubmit={(event) => {
        event.preventDefault()
        save.mutate()
      }}
    >
      <Input aria-label="Identyfikator zlecenia" placeholder="shipment_id" value={shipmentId} onChange={(event) => setShipmentId(event.target.value)} required />
      <Input aria-label="Rodzaj zdarzenia" placeholder="departed" value={eventKind} onChange={(event) => setEventKind(event.target.value)} required />
      <Input aria-label="Czas zdarzenia" placeholder="occurred_at" value={occurredAt} onChange={(event) => setOccurredAt(event.target.value)} required />
      <Input aria-label="Pochodzenie zapisu" placeholder="source_ref" value={sourceRef} onChange={(event) => setSourceRef(event.target.value)} required />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz zdarzenie
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function TrackingPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const events = useQuery({
    queryKey: ["tracking-events", ctx.organizationId],
    queryFn: fetchTrackingEvents,
    enabled: ready,
    retry: false,
  })

  return (
    <div className="flex flex-col gap-4" data-tracking="board">
      <CatalogHeading
        title="Tracking"
        subtitle="tracking M-36 · zdarzenia na zleceniu · nie mapa"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {events.isError ? <CatalogError error={events.error} /> : null}
      <TrackingEventForm organizationId={ctx.organizationId} />
      {(events.data ?? []).map((row) => (
        <p key={row.id} className="text-xs">
          {row.event_kind} {row.occurred_at}{" "}
          <Link className="underline" to="/shipments">
            zlecenie
          </Link>
        </p>
      ))}
    </div>
  )
}
