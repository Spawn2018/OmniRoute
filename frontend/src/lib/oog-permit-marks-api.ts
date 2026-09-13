import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OogPermitMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  permit_kind: string
  source_ref: string
}

export type OogPermitMarkPayload = {
  mark_code: string
  permit_kind: string
  source_ref: string
}

const PATH = "/api/v1/oog-permit-marks"

export function makeOogPermitMarkPayload(
  markCode: string,
  permitKind: string,
  sourceRef: string,
): OogPermitMarkPayload {
  return {
    mark_code: markCode.trim(),
    permit_kind: permitKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadOogPermitMarks(): Promise<OogPermitMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu zezwoleń OOG"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as OogPermitMarkRow[]
}

export async function createOogPermitMark(
  payload: OogPermitMarkPayload,
): Promise<OogPermitMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "oog-permit-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika zezwolenia OOG"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as OogPermitMarkRow
}
