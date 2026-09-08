import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type GroupageLineRow = {
  id: string
  organization_id: string
  line_code: string
  origin_location_id: string
  destination_location_id: string
  cutoff_local: string
  transit_days: number
  operating_dows: number[]
  source_ref: string
  superseded_by: string | null
}

export type GroupageLineWrite = {
  line_code: string
  origin_location_id: string
  destination_location_id: string
  cutoff_local: string
  transit_days: number
  operating_dows: number[]
  source_ref: string
}

const PATH = "/api/v1/groupage-lines"

export function groupageLineWrite(args: {
  code: string
  originId: string
  destId: string
  cutoff: string
  days: string
  dows: readonly number[]
  sourceRef: string
}): GroupageLineWrite {
  const clock = args.cutoff.trim()
  return {
    line_code: args.code.trim(),
    origin_location_id: args.originId.trim(),
    destination_location_id: args.destId.trim(),
    cutoff_local: clock.length === 5 ? `${clock}:00` : clock,
    transit_days: Number.parseInt(args.days.trim(), 10),
    operating_dows: [...args.dows],
    source_ref: args.sourceRef.trim(),
  }
}

export async function fetchGroupageLines(): Promise<GroupageLineRow[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy linii drobnicy"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as GroupageLineRow[]
}

export async function saveGroupageLine(payload: GroupageLineWrite): Promise<GroupageLineRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu linii drobnicy"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as GroupageLineRow
}
