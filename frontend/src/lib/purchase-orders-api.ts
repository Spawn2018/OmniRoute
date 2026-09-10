import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const HEADER_PATH = "/api/v1/purchase-orders"

export type PurchaseOrderRow = {
  id: string
  organization_id: string
  po_code: string
  plant_label: string | null
  source_ref: string
}

export type PurchaseOrderBody = {
  po_code: string
  plant_label: string | null
  source_ref: string
}

export function purchaseOrderBody(draft: {
  poSlug: string
  plantText: string
  originPointer: string
}): PurchaseOrderBody {
  const plant = draft.plantText.trim()
  return {
    po_code: draft.poSlug.trim(),
    plant_label: plant.length === 0 ? null : plant,
    source_ref: draft.originPointer.trim(),
  }
}

async function readPurchaseOrderJson<T>(response: Response, fallback: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function listPurchaseOrders(): Promise<PurchaseOrderRow[]> {
  const listed = await fetch(HEADER_PATH, { headers: requireAuthHeaders() })
  return readPurchaseOrderJson(listed, "Błąd listy zamówień zakupu", 200)
}

export async function persistPurchaseOrder(payload: PurchaseOrderBody): Promise<PurchaseOrderRow> {
  const posted = await fetch(HEADER_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return readPurchaseOrderJson(posted, "Błąd zapisu zamówienia zakupu", 201)
}
