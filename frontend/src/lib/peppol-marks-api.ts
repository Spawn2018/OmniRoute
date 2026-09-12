import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PeppolMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  peppol_kind: string
  source_ref: string
}

export type PeppolCreate = {
  mark_code: string
  peppol_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/peppol-marks"

export function toPeppolCreate(
  codeRaw: string,
  kindRaw: string,
  refRaw: string,
): PeppolCreate {
  return {
    mark_code: codeRaw.trim(),
    peppol_kind: kindRaw.trim().toLowerCase(),
    source_ref: refRaw.trim(),
  }
}

export async function fetchPeppolMarks(): Promise<PeppolMarkRow[]> {
  const http = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  if (http.ok) return (await http.json()) as PeppolMarkRow[]
  throw new ApiError(
    await readApiDetail(http, "Katalog Peppol niedostępny"),
    httpErrorStatus(http),
  )
}

export async function postPeppolMark(body: PeppolCreate): Promise<PeppolMarkRow> {
  const http = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  if (http.status === 201) return (await http.json()) as PeppolMarkRow
  throw new ApiError(
    await readApiDetail(http, "Zapis znacznika Peppol nieudany"),
    httpErrorStatus(http),
  )
}
