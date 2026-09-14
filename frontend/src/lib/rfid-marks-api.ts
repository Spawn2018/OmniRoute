import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type RfidMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  rfid_kind: string
  source_ref: string
}

export type RfidMarkPayload = {
  mark_code: string
  rfid_kind: string
  source_ref: string
}

const PATH = "/api/v1/rfid-marks"

export function buildRfidMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): RfidMarkPayload {
  return {
    mark_code: args.code.trim(),
    rfid_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchRfidMarks(): Promise<RfidMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu RFID"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as RfidMarkRow[]
}

export async function saveRfidMark(payload: RfidMarkPayload): Promise<RfidMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "rfid-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika RFID"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as RfidMarkRow
}
