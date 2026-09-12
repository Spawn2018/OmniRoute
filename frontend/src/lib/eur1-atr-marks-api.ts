import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Eur1AtrMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  cert_kind: string
  source_ref: string
}

export type Eur1AtrPayload = {
  mark_code: string
  cert_kind: string
  source_ref: string
}

const PATH = "/api/v1/eur1-atr-marks"

export function makeEur1AtrPayload(
  code: string,
  kind: string,
  ref: string,
): Eur1AtrPayload {
  return {
    mark_code: code.trim(),
    cert_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadEur1AtrMarks(): Promise<Eur1AtrMarkRow[]> {
  const res = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Lista znacznikow EUR.1/ATR niedostepna"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as Eur1AtrMarkRow[]
}

export async function createEur1AtrMark(
  body: Eur1AtrPayload,
): Promise<Eur1AtrMarkRow> {
  const res = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Zapis znacznika EUR.1/ATR nieudany"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as Eur1AtrMarkRow
}
