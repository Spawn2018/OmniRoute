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
  source_ref: string
  superseded_by: string | null
}

export type TripWrite = {
  trip_no: string
  status: string
  vehicle_id: string | null
  trailer_id: string | null
  driver_id: string | null
  source_ref: string
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
}): TripWrite {
  return {
    trip_no: args.number.trim(),
    status: args.state.trim(),
    vehicle_id: optionalId(args.vehicle),
    trailer_id: optionalId(args.trailer),
    driver_id: optionalId(args.driver),
    source_ref: "tenant:manual",
  }
}

export async function fetchTrips(state: string): Promise<TripRow[]> {
  const query = new URLSearchParams()
  if (state !== "") {
    query.set("status", state)
  }
  const suffix = query.size === 0 ? "" : `?${query}`
  const reply = await fetch(`${PATH}${suffix}`, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy przejazdów"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as TripRow[]
}

export async function saveTrip(payload: TripWrite): Promise<TripRow> {
  const auth = requireAuthHeaders()
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      Authorization: auth.Authorization,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu przejazdu"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as TripRow
}
