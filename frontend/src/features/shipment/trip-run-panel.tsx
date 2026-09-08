import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchTrips, saveTrip, tripWrite } from "@/lib/trips-api"
import { getTenantContext } from "@/lib/tenant"

const STATES = [
  { token: "draft", label: "szkic" },
  { token: "planned", label: "zaplanowany" },
  { token: "in_transit", label: "w drodze" },
  { token: "completed", label: "zakończony" },
  { token: "cancelled", label: "anulowany" },
] as const

export function TripRunPanel(args: { signedIn: boolean }) {
  const ctx = getTenantContext()
  const cache = useQueryClient()
  const [number, setNumber] = useState("")
  const [state, setState] = useState("draft")
  const [vehicle, setVehicle] = useState("")
  const [trailer, setTrailer] = useState("")
  const [driver, setDriver] = useState("")
  const listed = useQuery({
    queryKey: ["trips", ctx.organizationId, state],
    queryFn: () => fetchTrips(state),
    enabled: args.signedIn,
    retry: false,
  })
  const persist = useMutation({
    mutationFn: () =>
      saveTrip(tripWrite({ number, state, vehicle, trailer, driver })),
    onSuccess: () => {
      void cache.invalidateQueries({ queryKey: ["trips", ctx.organizationId, state] })
    },
  })
  return (
    <section className="grid gap-2 rounded-md border border-border p-3" data-trip="run">
      <h2 className="text-sm font-medium">Przejazd</h2>
      <p className="text-xs text-muted-foreground">
        Numer i status. Flota opcjonalna. Nie km. Nie mapa.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Numer przejazdu
        <Input
          aria-label="Numer przejazdu"
          placeholder="trip_no"
          value={number}
          onChange={(event) => setNumber(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Status przejazdu
        <select
          aria-label="Status przejazdu"
          className="h-8 rounded-md border border-border bg-background px-2 text-sm"
          value={state}
          onChange={(event) => setState(event.target.value)}
        >
          {STATES.map((entry) => (
            <option key={entry.token} value={entry.token}>
              {entry.label}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pojazd (opcjonalnie)
        <Input
          aria-label="Identyfikator pojazdu przejazdu"
          placeholder="vehicle_id"
          value={vehicle}
          onChange={(event) => setVehicle(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Naczepa (opcjonalnie)
        <Input
          aria-label="Identyfikator naczepy przejazdu"
          placeholder="trailer_id"
          value={trailer}
          onChange={(event) => setTrailer(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kierowca (opcjonalnie)
        <Input
          aria-label="Identyfikator kierowcy przejazdu"
          placeholder="driver_id"
          value={driver}
          onChange={(event) => setDriver(event.target.value)}
        />
      </label>
      <Button
        type="button"
        disabled={!args.signedIn || number.trim() === "" || persist.isPending}
        onClick={() => persist.mutate()}
      >
        Zapisz przejazd
      </Button>
      {persist.isError ? (
        <p className="text-sm text-destructive">{(persist.error as Error).message}</p>
      ) : null}
      <ul className="space-y-1">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.trip_no} · {row.status}
          </li>
        ))}
      </ul>
    </section>
  )
}
