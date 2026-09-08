import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type StopRow = {
  id: string
  organization_id: string
  shipment_id: string
  location_id: string
  stop_kind: string
  sequence_no: number
  time_zone: string
  status: string
  source_ref: string
  superseded_by: string | null
}

export type StopWrite = {
  shipment_id: string
  location_id: string
  stop_kind: string
  sequence_no: number
  time_zone: string
  status: string
  source_ref: string
}

const PATH = "/api/v1/stops"

export function stopWrite(args: {
  shipmentId: string
  locationId: string
  stopKind: string
  sequenceNo: number
  timeZone: string
  status: string
}): StopWrite {
  return {
    shipment_id: args.shipmentId.trim(),
    location_id: args.locationId.trim(),
    stop_kind: args.stopKind.trim(),
    sequence_no: args.sequenceNo,
    time_zone: args.timeZone.trim(),
    status: args.status.trim(),
    source_ref: "tenant:manual",
  }
}

export async function fetchStops(shipmentId: string): Promise<StopRow[]> {
  const query = new URLSearchParams({ shipment_id: shipmentId })
  const reply = await fetch(`${PATH}?${query}`, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy punktów"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as StopRow[]
}

export async function saveStop(payload: StopWrite): Promise<StopRow> {
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
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu punktu"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as StopRow
}
