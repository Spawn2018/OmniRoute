import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/cod-instructions"

export type CodMark = {
  id: string
  organization_id: string
  shipment_id: string
  instruction_code: string
  collection_status: string
  source_ref: string
}

export type CodMarkWrite = {
  shipment_id: string
  instruction_code: string
  collection_status: string
  source_ref: string
}

export function collectionWrite(args: {
  haulToken: string
  markerToken: string
  cashStage: string
  originStamp: string
}): CodMarkWrite {
  return {
    shipment_id: args.haulToken.trim(),
    instruction_code: args.markerToken.trim(),
    collection_status: args.cashStage.trim(),
    source_ref: args.originStamp.trim(),
  }
}

export async function listCodMarks(): Promise<CodMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy pobrań"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as CodMark[]
}

export async function persistCodMark(payload: CodMarkWrite): Promise<CodMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "cod-mark",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu pobrania"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as CodMark
}
