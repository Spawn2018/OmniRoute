import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/bonded-marks"

export type BondedMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  bond_kind: string
  source_ref: string
}

export type BondedMarkWrite = {
  mark_code: string
  bond_kind: string
  source_ref: string
}

export function buildBondedMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): BondedMarkWrite {
  return {
    mark_code: fields.code.trim(),
    bond_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchBondedMarks(): Promise<BondedMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników bonded", 200)
}

export async function saveBondedMark(body: BondedMarkWrite): Promise<BondedMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika bonded", 201)
}
