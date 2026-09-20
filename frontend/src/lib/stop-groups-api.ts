import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/stop-groups"

export type StopGroupMark = {
  id: string
  organization_id: string
  shipment_id: string
  group_code: string
  source_ref: string
}

export type StopGroupWrite = {
  shipment_id: string
  group_code: string
  source_ref: string
}

export function groupWrite(args: {
  shipmentToken: string
  groupCode: string
  originStamp: string
}): StopGroupWrite {
  return {
    shipment_id: args.shipmentToken.trim(),
    group_code: args.groupCode.trim(),
    source_ref: args.originStamp.trim(),
  }
}

export async function listStopGroups(): Promise<StopGroupMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy grup punktów"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as StopGroupMark[]
}

export async function persistStopGroup(payload: StopGroupWrite): Promise<StopGroupMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "stop-group-mark",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu grupy punktów"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as StopGroupMark
}
