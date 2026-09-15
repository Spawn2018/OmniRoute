import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CfoNarrativeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  narrative_kind: string
  source_ref: string
}

export type CfoNarrativeMarkPayload = {
  mark_code: string
  narrative_kind: string
  source_ref: string
}

const PATH = "/api/v1/cfo-narrative-marks"

export function buildCfoNarrativeMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): CfoNarrativeMarkPayload {
  return {
    mark_code: args.code.trim(),
    narrative_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchCfoNarrativeMarks(): Promise<CfoNarrativeMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu narracji CFO"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as CfoNarrativeMarkRow[]
}

export async function saveCfoNarrativeMark(
  payload: CfoNarrativeMarkPayload,
): Promise<CfoNarrativeMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "cfo-narrative-mark-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika narracji CFO"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as CfoNarrativeMarkRow
}
