import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/shipment-packages"

export type ParcelRow = {
  id: string
  organization_id: string
  shipment_id: string
  stop_id: string
  package_code: string
  package_status: string
  scan_token: string
  source_ref: string
}

export type ParcelWrite = {
  shipment_id: string
  stop_id: string
  package_code: string
  package_status: string
  scan_token: string
  source_ref: string
}

export function parcelWrite(args: {
  orderKey: string
  haltRef: string
  parcelToken: string
  stageMark: string
  scanMark: string
  originNote: string
}): ParcelWrite {
  return {
    shipment_id: args.orderKey.trim(),
    stop_id: args.haltRef.trim(),
    package_code: args.parcelToken.trim(),
    package_status: args.stageMark.trim(),
    scan_token: args.scanMark.trim(),
    source_ref: args.originNote.trim(),
  }
}

export async function listParcels(): Promise<ParcelRow[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy paczek"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as ParcelRow[]
}

export async function persistParcel(payload: ParcelWrite): Promise<ParcelRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "parcel-scan",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd skanu paczki"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as ParcelRow
}
