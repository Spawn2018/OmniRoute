import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type NacMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  nac_kind: string
  source_ref: string
}

export type NacMarkPayload = {
  mark_code: string
  nac_kind: string
  source_ref: string
}

const PATH = "/api/v1/nac-marks"

export function buildNacMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): NacMarkPayload {
  return {
    mark_code: args.code.trim(),
    nac_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchNacMarks(): Promise<NacMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu NAC"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as NacMarkRow[]
}

export async function saveNacMark(payload: NacMarkPayload): Promise<NacMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "nac-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać stance NAC"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as NacMarkRow
}
