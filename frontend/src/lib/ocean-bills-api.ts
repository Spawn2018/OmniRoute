import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/ocean-bills"

export type HouseMark = {
  id: string
  organization_id: string
  shipment_id: string
  bill_no: string | null
  bill_kind: string
  source_ref: string
}

export type HouseMarkWrite = {
  shipment_id: string
  bill_no?: string
  bill_kind: string
  source_ref: string
}

export function ladingWrite(args: {
  consignmentToken: string
  houseToken: string
  kindToken: string
  originStamp: string
}): HouseMarkWrite {
  const house = args.houseToken.trim()
  return {
    shipment_id: args.consignmentToken.trim(),
    ...(house !== "" ? { bill_no: house } : {}),
    bill_kind: args.kindToken.trim(),
    source_ref: args.originStamp.trim(),
  }
}

export async function listHouseMarks(): Promise<HouseMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy konosamentów"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as HouseMark[]
}

export async function persistHouseMark(payload: HouseMarkWrite): Promise<HouseMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "house-mark",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu konosamentu"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as HouseMark
}

async function issueBillNumber(
  billId: string,
  kind: "hbl" | "mbl",
): Promise<HouseMark> {
  const suffix = kind === "hbl" ? "hbl-number" : "mbl-number"
  const reply = await fetch(`${PATH}/${billId}/${suffix}`, {
    method: "POST",
    headers: requireAuthHeaders(),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd nadania numeru"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as HouseMark
}

export function issueHblNumber(billId: string): Promise<HouseMark> {
  return issueBillNumber(billId, "hbl")
}

export function issueMblNumber(billId: string): Promise<HouseMark> {
  return issueBillNumber(billId, "mbl")
}
