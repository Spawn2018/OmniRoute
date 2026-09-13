import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PoFinancingMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  financing_kind: string
  source_ref: string
}

export type PoFinancingMarkPayload = {
  mark_code: string
  financing_kind: string
  source_ref: string
}

const PATH = "/api/v1/po-financing-marks"

export function buildPoFinancingMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): PoFinancingMarkPayload {
  return {
    mark_code: args.code.trim(),
    financing_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchPoFinancingMarks(): Promise<PoFinancingMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu PO Financing"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as PoFinancingMarkRow[]
}

export async function savePoFinancingMark(
  payload: PoFinancingMarkPayload,
): Promise<PoFinancingMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "po-financing-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać stance PO Financing"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as PoFinancingMarkRow
}
