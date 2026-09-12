import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type EccnMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  control_kind: string
  source_ref: string
}

export type EccnPayload = {
  mark_code: string
  control_kind: string
  source_ref: string
}

const URL = "/api/v1/eccn-marks"

export function makeEccnPayload(
  code: string,
  kind: string,
  ref: string,
): EccnPayload {
  return {
    mark_code: code.trim(),
    control_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadEccnMarks(): Promise<EccnMarkRow[]> {
  const res = await fetch(URL, { headers: requireAuthHeaders() })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Lista znacznikow ECCN niedostepna"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as EccnMarkRow[]
}

export async function createEccnMark(body: EccnPayload): Promise<EccnMarkRow> {
  const res = await fetch(URL, {
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
      await readApiDetail(res, "Zapis znacznika ECCN nieudany"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as EccnMarkRow
}
