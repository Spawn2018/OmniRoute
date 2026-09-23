import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type TripVarianceMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  variance_kind: string
  source_ref: string
}

export type TripVarianceMarkWrite = {
  mark_code: string
  variance_kind: string
  source_ref: string
}

const ROOT = "/api/v1/trip-variance-marks" as const

function authJsonHeaders(): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    "Content-Type": "application/json",
  }
}

export function buildTripVarianceMarkWrite(
  code: string,
  kind: string,
  origin: string,
): TripVarianceMarkWrite {
  return {
    mark_code: code.trim(),
    variance_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function decodeOk<T>(response: Response, whenFail: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
}

export async function fetchTripVarianceMarks(): Promise<TripVarianceMarkRow[]> {
  const response = await fetch(ROOT, { headers: requireAuthHeaders() })
  return decodeOk(response, "Błąd listy wiązań przekazania", 200)
}

export async function saveTripVarianceMark(
  payload: TripVarianceMarkWrite,
): Promise<TripVarianceMarkRow> {
  const response = await fetch(ROOT, {
    method: "POST",
    headers: authJsonHeaders(),
    body: JSON.stringify(payload),
  })
  return decodeOk(response, "Błąd zapisu wariancji przejazdu", 201)
}
