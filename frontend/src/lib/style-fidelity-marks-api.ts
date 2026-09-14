import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type StyleFidelityMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  fidelity_kind: string
  source_ref: string
}

export type StyleFidelityMarkPayload = {
  mark_code: string
  fidelity_kind: string
  source_ref: string
}

const PATH = "/api/v1/style-fidelity-marks"

export function buildStyleFidelityMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): StyleFidelityMarkPayload {
  return {
    mark_code: args.code.trim(),
    fidelity_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchStyleFidelityMarks(): Promise<StyleFidelityMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu fidelity"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as StyleFidelityMarkRow[]
}

export async function saveStyleFidelityMark(
  payload: StyleFidelityMarkPayload,
): Promise<StyleFidelityMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "style-fidelity-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać stancji fidelity"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as StyleFidelityMarkRow
}
