import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type TripBillMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  bill_kind: string
  source_ref: string
}

export type TripBillMarkPayload = {
  mark_code: string
  bill_kind: string
  source_ref: string
}

const PATH = "/api/v1/trip-bill-marks"

export function buildTripBillMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): TripBillMarkPayload {
  return {
    mark_code: args.code.trim(),
    bill_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchTripBillMarks(): Promise<TripBillMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu gotowości do FV"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as TripBillMarkRow[]
}

export async function saveTripBillMark(
  payload: TripBillMarkPayload,
): Promise<TripBillMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "trip-bill-mark-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika gotowości do FV"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as TripBillMarkRow
}
