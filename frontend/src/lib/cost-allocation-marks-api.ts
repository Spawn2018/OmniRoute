import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const COST_ALLOCATION_MARKS_PATH = "/api/v1/cost-allocation-marks"

export type CostAllocationMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  alloc_kind: string
  source_ref: string
}

export type CostAllocationMarkWrite = {
  mark_code: string
  alloc_kind: string
  source_ref: string
}

export function buildCostAllocationMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): CostAllocationMarkWrite {
  const mark_code = fields.code.trim()
  const alloc_kind = fields.kind.trim().toLowerCase()
  const source_ref = fields.origin.trim()
  return { mark_code, alloc_kind, source_ref }
}

async function parseCostAllocationJson<T>(
  response: Response,
  failMessage: string,
  expectedStatus: number,
): Promise<T> {
  if (response.status !== expectedStatus) {
    const detail = await readApiDetail(response, failMessage)
    throw new ApiError(detail, httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCostAllocationMarks(): Promise<CostAllocationMarkRow[]> {
  const response = await fetch(COST_ALLOCATION_MARKS_PATH, { headers: requireAuthHeaders() })
  return parseCostAllocationJson(response, "Błąd listy znaczników cost allocation", 200)
}

export async function saveCostAllocationMark(
  body: CostAllocationMarkWrite,
): Promise<CostAllocationMarkRow> {
  const response = await fetch(COST_ALLOCATION_MARKS_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return parseCostAllocationJson(response, "Błąd zapisu znacznika cost allocation", 201)
}
