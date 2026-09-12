import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type VdaOdetteMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  edi_kind: string
  source_ref: string
}

export type VdaOdettePayload = {
  mark_code: string
  edi_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/vda-odette-marks"

export function makeVdaOdettePayload(
  code: string,
  kind: string,
  ref: string,
): VdaOdettePayload {
  return {
    mark_code: code.trim(),
    edi_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadVdaOdetteMarks(): Promise<VdaOdetteMarkRow[]> {
  const msg = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (msg.ok) {
    return (await msg.json()) as VdaOdetteMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(msg, "Lista znacznikow VDA/Odette niedostepna"),
    httpErrorStatus(msg),
  )
}

export async function createVdaOdetteMark(
  payload: VdaOdettePayload,
): Promise<VdaOdetteMarkRow> {
  const msg = await fetch(ROUTE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (msg.status === 201) {
    return (await msg.json()) as VdaOdetteMarkRow
  }
  throw new ApiError(
    await readApiDetail(msg, "Zapis znacznika VDA/Odette nieudany"),
    httpErrorStatus(msg),
  )
}
