import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FieldCarryForwardRow = {
  id: string
  organization_id: string
  quotation_id: string
  shipment_id: string
  field_key: string
  field_value: string
  superseded_by: string | null
}

export type FieldCarryForwardCreateBody = {
  quotation_id: string
  shipment_id: string
  fields: Record<string, string>
}

const PATH = "/api/v1/field-carry-forwards"

export function fieldCarryForwardBody(args: {
  quotationId: string
  shipmentId: string
  incoterm: string | null
  tradeSide: string | null
  namedPlace: string | null
}): FieldCarryForwardCreateBody {
  const fields: Record<string, string> = {}
  const incoterm = args.incoterm?.trim() ?? ""
  const tradeSide = args.tradeSide?.trim() ?? ""
  if (incoterm !== "") fields.incoterm = incoterm
  if (tradeSide !== "") fields.trade_side = tradeSide
  if (args.namedPlace !== null) fields.named_place = args.namedPlace.trim()
  return {
    quotation_id: args.quotationId,
    shipment_id: args.shipmentId,
    fields,
  }
}

export async function fetchFieldCarryForwards(shipmentId: string): Promise<FieldCarryForwardRow[]> {
  const query = new URLSearchParams({ shipment_id: shipmentId })
  const reply = await fetch(`${PATH}?${query}`, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy przeniesienia"), httpErrorStatus(reply))
  }
  return (await reply.json()) as FieldCarryForwardRow[]
}

export async function saveFieldCarryForwards(
  payload: FieldCarryForwardCreateBody,
): Promise<FieldCarryForwardRow[]> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: new Headers({
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(payload),
  })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd przeniesienia pól"), httpErrorStatus(reply))
  }
  return (await reply.json()) as FieldCarryForwardRow[]
}
