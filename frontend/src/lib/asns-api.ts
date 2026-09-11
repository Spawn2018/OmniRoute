import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const ASN_PATH = "/api/v1/asns"

export type AsnRow = {
  id: string
  organization_id: string
  purchase_order_id: string
  asn_code: string
  plant_label: string | null
  carrier_label: string | null
  ship_ref_label: string | null
  guide_code: string | null
  source_ref: string
}

export type AsnBody = {
  purchase_order_id: string
  asn_code: string
  plant_label: string | null
  carrier_label: string | null
  ship_ref_label: string | null
  guide_code: string | null
  source_ref: string
}

function optionalLabel(raw: string): string | null {
  const label = raw.trim()
  return label.length === 0 ? null : label
}

export function asnBody(draft: {
  purchaseOrderId: string
  asnSlug: string
  plantText: string
  carrierText: string
  shipRefText: string
  guideSlug: string
  originPointer: string
}): AsnBody {
  return {
    purchase_order_id: draft.purchaseOrderId.trim(),
    asn_code: draft.asnSlug.trim(),
    plant_label: optionalLabel(draft.plantText),
    carrier_label: optionalLabel(draft.carrierText),
    ship_ref_label: optionalLabel(draft.shipRefText),
    guide_code: optionalLabel(draft.guideSlug),
    source_ref: draft.originPointer.trim(),
  }
}

async function readAsnJson<T>(response: Response, fallback: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function listAsns(): Promise<AsnRow[]> {
  const listed = await fetch(ASN_PATH, { headers: requireAuthHeaders() })
  return readAsnJson(listed, "Błąd listy awiz wysyłki", 200)
}

export async function persistAsn(payload: AsnBody): Promise<AsnRow> {
  const posted = await fetch(ASN_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return readAsnJson(posted, "Błąd zapisu awiza wysyłki", 201)
}
