import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Money } from "@/components/money"
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

function needsFreeze(state: string): boolean {
  return state === "in_transit" || state === "completed"
}

export function TripRunPanel(args: { signedIn: boolean }) {
  const ctx = getTenantContext()
  const cache = useQueryClient()
  const [number, setNumber] = useState("")
  const [state, setState] = useState("draft")
  const [vehicle, setVehicle] = useState("")
  const [trailer, setTrailer] = useState("")
  const [driver, setDriver] = useState("")
  const [driver2, setDriver2] = useState("")
  const [buyAmount, setBuyAmount] = useState("")
  const [buyCurrency, setBuyCurrency] = useState("EUR")
  const listed = useQuery({
    queryKey: ["trips", ctx.organizationId, state],
    queryFn: () => fetchTrips(state),
    enabled: args.signedIn,
    retry: false,
  })
  const persist = useMutation({
    mutationFn: () =>
      saveTrip(
        tripWrite({
          number,
          state,
          vehicle,
          trailer,
          driver,
          driver2,
          buyAmount,
          buyCurrency,
        }),
      ),
    onSuccess: () => {
      void cache.invalidateQueries({ queryKey: ["trips", ctx.organizationId, state] })
    },
  })
  return (
    <section className="grid gap-2 rounded-md border border-border p-3" data-trip="run">
      <h2 className="text-sm font-medium">Przejazd</h2>
      <p className="text-xs text-muted-foreground">
        Numer i status. Snapshot kupna przy w drodze. Flota opcjonalna, w tym drugi kierowca.
        Nie km. Nie wariancja.
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
          <option value={STATES[0].token}>{STATES[0].label}</option>
          <option value={STATES[1].token}>{STATES[1].label}</option>
          <option value={STATES[2].token}>{STATES[2].label}</option>
          <option value={STATES[3].token}>{STATES[3].label}</option>
          <option value={STATES[4].token}>{STATES[4].label}</option>
        </select>
      </label>
      {needsFreeze(state) ? (
        <>
          <label className="flex flex-col gap-1 text-xs">
            Snapshot kosztu kupna
            <Input
              aria-label="Snapshot kosztu kupna"
              placeholder="expected_buy_amount"
              value={buyAmount}
              onChange={(event) => setBuyAmount(event.target.value)}
            />
          </label>
          <label className="flex flex-col gap-1 text-xs">
            Waluta snapshotu
            <Input
              aria-label="Waluta snapshotu"
              placeholder="EUR"
              value={buyCurrency}
              onChange={(event) => setBuyCurrency(event.target.value)}
            />
          </label>
        </>
      ) : null}
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
      <label className="flex flex-col gap-1 text-xs">
        Drugi kierowca (opcjonalnie)
        <Input
          aria-label="Identyfikator drugiego kierowcy przejazdu"
          placeholder="driver2_id"
          value={driver2}
          onChange={(event) => setDriver2(event.target.value)}
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
            {row.expected_buy_amount !== null && row.expected_buy_currency !== null ? (
              <>
                {" · "}
                <Money amount={row.expected_buy_amount} currency={row.expected_buy_currency} />
              </>
            ) : null}
          </li>
        ))}
      </ul>
    </section>
  )
}
