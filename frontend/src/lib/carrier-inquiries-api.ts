import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type InquiryMemberRank = {
  network_member_id: string
  answered_count: number
}

export type CarrierInquiry = {
  id: string
  organization_id: string
  network_member_id: string
  source_ref: string
  status: string
  origin_port_id: string | null
  destination_port_id: string | null
  quoted_amount: string | null
  quoted_currency: string | null
  quoted_transit_days: number | null
  no_reply_after: string | null
  party_id: string | null
  country_code: string | null
}

export function carrierInquiryBatchBody(input: {
  memberIds: readonly string[]
  status: string
  originPortId: string
  destinationPortId: string
}): {
  network_member_ids: string[]
  status: string
  origin_port_id?: string
  destination_port_id?: string
} {
  const body: {
    network_member_ids: string[]
    status: string
    origin_port_id?: string
    destination_port_id?: string
  } = {
    network_member_ids: input.memberIds.map((item) => item.trim()).filter((item) => item !== ""),
    status: input.status.trim(),
  }
  const origin = input.originPortId.trim()
  const dest = input.destinationPortId.trim()
  if (origin !== "") {
    body.origin_port_id = origin
  }
  if (dest !== "") {
    body.destination_port_id = dest
  }
  return body
}

async function readInquiry(response: Response, fallback: string): Promise<CarrierInquiry> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as CarrierInquiry
}

export function topRankedMemberIds(
  ranks: readonly InquiryMemberRank[],
  limit: number,
): string[] {
  return ranks.slice(0, limit).map((row) => row.network_member_id)
}

export function inquiryIdsForMembers(
  inquiries: readonly CarrierInquiry[],
  memberIds: readonly string[],
): string[] {
  const allowed = new Set(memberIds)
  return inquiries.filter((row) => allowed.has(row.network_member_id)).map((row) => row.id)
}

export async function fetchCarrierInquiryRanking(): Promise<InquiryMemberRank[]> {
  const response = await fetch("/api/v1/carrier-inquiries/ranking", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd rankingu zapytań"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as InquiryMemberRank[]
}

export async function fetchCarrierInquiries(
  silent?: "overdue",
  groupBy?: string,
): Promise<CarrierInquiry[]> {
  const params = new URLSearchParams()
  if (silent === "overdue") {
    params.set("silent", "overdue")
  }
  const token = groupBy?.trim() ?? ""
  if (token !== "") {
    params.set("group_by", token)
  }
  const suffix = params.toString() === "" ? "" : `?${params.toString()}`
  const response = await fetch(`/api/v1/carrier-inquiries${suffix}`, {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy zapytań do agentów"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CarrierInquiry[]
}

export async function createCarrierInquiry(
  networkMemberId: string,
  noReplyAfter = "",
): Promise<CarrierInquiry> {
  const body: { network_member_id: string; no_reply_after?: string } = {
    network_member_id: networkMemberId,
  }
  const silence = noReplyAfter.trim()
  if (silence !== "") {
    body.no_reply_after = silence
  }
  const response = await fetch("/api/v1/carrier-inquiries", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readInquiry(response, "Błąd zapisu zapytania do agenta")
}

export async function patchInquirySilence(
  inquiryId: string,
  noReplyAfter: string,
): Promise<CarrierInquiry> {
  const token = noReplyAfter.trim()
  const response = await fetch(`/api/v1/carrier-inquiries/${inquiryId}`, {
    method: "PATCH",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ no_reply_after: token === "" ? null : token }),
  })
  return readInquiry(response, "Błąd daty ciszy")
}

export async function createCarrierInquiryBatch(
  body: ReturnType<typeof carrierInquiryBatchBody>,
): Promise<CarrierInquiry[]> {
  const response = await fetch("/api/v1/carrier-inquiries/batch", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu paczki zapytań"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CarrierInquiry[]
}
