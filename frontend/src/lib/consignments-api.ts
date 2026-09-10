import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/consignments"

export type ParcelMark = {
  id: string
  organization_id: string
  shipment_id: string
  consignment_ref: string
  source_ref: string
}

export type ParcelMarkWrite = {
  shipment_id: string
  consignment_ref: string
  source_ref: string
}

export function parcelWrite(args: {
  shipmentToken: string
  parcelRef: string
  originStamp: string
}): ParcelMarkWrite {
  return {
    shipment_id: args.shipmentToken.trim(),
    consignment_ref: args.parcelRef.trim(),
    source_ref: args.originStamp.trim(),
  }
}

export async function listParcels(): Promise<ParcelMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy przesyłek"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as ParcelMark[]
}

export async function persistParcel(payload: ParcelMarkWrite): Promise<ParcelMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "consignment-mark",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu przesyłki"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as ParcelMark
}
