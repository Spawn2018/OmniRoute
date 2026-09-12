import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type InventoryPositionMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  stock_kind: string
  source_ref: string
}

export type InventoryPositionPayload = {
  mark_code: string
  stock_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/inventory-position-marks"

export function makeInventoryPositionPayload(
  code: string,
  kind: string,
  ref: string,
): InventoryPositionPayload {
  return {
    mark_code: code.trim(),
    stock_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadInventoryPositionMarks(): Promise<
  InventoryPositionMarkRow[]
> {
  const msg = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (msg.ok) {
    return (await msg.json()) as InventoryPositionMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(msg, "Lista znacznikow inventory position niedostepna"),
    httpErrorStatus(msg),
  )
}

export async function createInventoryPositionMark(
  payload: InventoryPositionPayload,
): Promise<InventoryPositionMarkRow> {
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
    return (await msg.json()) as InventoryPositionMarkRow
  }
  throw new ApiError(
    await readApiDetail(msg, "Zapis znacznika inventory position nieudany"),
    httpErrorStatus(msg),
  )
}
