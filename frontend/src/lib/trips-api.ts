import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type TripRow = {
  id: string
  organization_id: string
  trip_no: string
  status: string
  vehicle_id: string | null
  trailer_id: string | null
  driver_id: string | null
  driver2_id: string | null
  source_ref: string
  expected_buy_amount: string | null
  expected_buy_currency: string | null
  route_label: string | null
  planned_distance_km: string | null
  superseded_by: string | null
}

export type TripWrite = {
  trip_no: string
  status: string
  vehicle_id: string | null
  trailer_id: string | null
  driver_id: string | null
  driver2_id: string | null
  source_ref: string
  expected_buy_amount: string | null
  expected_buy_currency: string | null
  route_label: string | null
  planned_distance_km: string | null
}

const PATH = "/api/v1/trips"

function optionalId(raw: string): string | null {
  const token = raw.trim()
  return token === "" ? null : token
}

export function tripWrite(args: {
  number: string
  state: string
  vehicle: string
  trailer: string
  driver: string
  driver2: string
  routeLabel: string
  plannedDistance: string
  buyAmount: string
  buyCurrency: string
}): TripWrite {
  const freeze = args.state === "in_transit" || args.state === "completed"
  const planned = args.plannedDistance.trim()
  return {
    trip_no: args.number.trim(),
    status: args.state.trim(),
    vehicle_id: optionalId(args.vehicle),
    trailer_id: optionalId(args.trailer),
    driver_id: optionalId(args.driver),
    driver2_id: optionalId(args.driver2),
    source_ref: "tenant:manual",
    expected_buy_amount: freeze ? args.buyAmount.trim() : null,
    expected_buy_currency: freeze ? args.buyCurrency.trim() : null,
    route_label: optionalId(args.routeLabel),
    planned_distance_km: planned === "" ? null : planned,
  }
}

export async function fetchTrips(state: string): Promise<TripRow[]> {
  const suffix = state === "" ? "" : `?status=${encodeURIComponent(state)}`
  const reply = await fetch(`${PATH}${suffix}`, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy przejazdów"), httpErrorStatus(reply))
  }
  return (await reply.json()) as TripRow[]
}

export async function saveTrip(payload: TripWrite): Promise<TripRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu przejazdu"), httpErrorStatus(reply))
  }
  return (await reply.json()) as TripRow
}
