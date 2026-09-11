import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const LINE_PATH = "/api/v1/po-lines"

export type PoLineRow = {
  id: string
  organization_id: string
  purchase_order_id: string
  line_code: string
  sku_code: string
  qty: string
  uom_code: string
  plant_label: string | null
  batch_label: string | null
  serial_label: string | null
  coo_label: string | null
  source_ref: string
}

export type PoLineBody = {
  purchase_order_id: string
  line_code: string
  sku_code: string
  qty: string
  uom_code: string
  plant_label: string | null
  batch_label: string | null
  serial_label: string | null
  coo_label: string | null
  source_ref: string
}

function optionalLabel(raw: string): string | null {
  const label = raw.trim()
  return label.length === 0 ? null : label
}

export function poLineBody(draft: {
  purchaseOrderId: string
  lineSlug: string
  skuText: string
  qtyText: string
  uomText: string
  plantText: string
  batchText: string
  serialText: string
  cooText: string
  originPointer: string
}): PoLineBody {
  return {
    purchase_order_id: draft.purchaseOrderId.trim(),
    line_code: draft.lineSlug.trim(),
    sku_code: draft.skuText.trim(),
    qty: draft.qtyText.trim(),
    uom_code: draft.uomText.trim(),
    plant_label: optionalLabel(draft.plantText),
    batch_label: optionalLabel(draft.batchText),
    serial_label: optionalLabel(draft.serialText),
    coo_label: optionalLabel(draft.cooText),
    source_ref: draft.originPointer.trim(),
  }
}

async function readPoLineJson<T>(response: Response, fallback: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function listPoLines(): Promise<PoLineRow[]> {
  const listed = await fetch(LINE_PATH, { headers: requireAuthHeaders() })
  return readPoLineJson(listed, "Błąd listy linii zamówienia", 200)
}

export async function persistPoLine(payload: PoLineBody): Promise<PoLineRow> {
  const posted = await fetch(LINE_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return readPoLineJson(posted, "Błąd zapisu linii zamówienia", 201)
}
