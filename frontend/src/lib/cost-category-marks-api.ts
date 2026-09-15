import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const COST_CATEGORY_MARKS_PATH = "/api/v1/cost-category-marks"

export type CostCategoryMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  category_kind: string
  source_ref: string
}

export type CostCategoryMarkWrite = {
  mark_code: string
  category_kind: string
  source_ref: string
}

export function buildCostCategoryMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): CostCategoryMarkWrite {
  const mark_code = fields.code.trim()
  const category_kind = fields.kind.trim().toLowerCase()
  const source_ref = fields.origin.trim()
  return { mark_code, category_kind, source_ref }
}

async function parseCostCategoryJson<T>(
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

export async function fetchCostCategoryMarks(): Promise<CostCategoryMarkRow[]> {
  const response = await fetch(COST_CATEGORY_MARKS_PATH, { headers: requireAuthHeaders() })
  return parseCostCategoryJson(response, "Błąd listy znaczników cost category", 200)
}

export async function saveCostCategoryMark(
  body: CostCategoryMarkWrite,
): Promise<CostCategoryMarkRow> {
  const response = await fetch(COST_CATEGORY_MARKS_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return parseCostCategoryJson(response, "Błąd zapisu znacznika cost category", 201)
}
