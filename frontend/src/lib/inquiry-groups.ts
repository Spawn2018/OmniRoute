import type { CarrierInquiry } from "@/lib/carrier-inquiries-api"

export const BUY_DESK_GROUP_BY = ["party", "country", "status", "thread"] as const

export type BuyDeskGroupBy = (typeof BUY_DESK_GROUP_BY)[number]

export const DEFAULT_BUY_DESK_GROUP_BY: BuyDeskGroupBy = "party"

export type BuyDeskInquiryGroup = {
  key: string
  rows: CarrierInquiry[]
}

export function buyDeskGroupByOrDefault(raw: string): BuyDeskGroupBy {
  const token = raw.trim()
  if (
    token === "country" ||
    token === "status" ||
    token === "party" ||
    token === "thread"
  ) {
    return token
  }
  return DEFAULT_BUY_DESK_GROUP_BY
}

export function groupCarrierInquiries(
  rows: readonly CarrierInquiry[],
  groupBy: BuyDeskGroupBy,
): BuyDeskInquiryGroup[] {
  const buckets = new Map<string, CarrierInquiry[]>()
  for (const row of rows) {
    const key = groupKey(row, groupBy)
    const bucket = buckets.get(key)
    if (bucket === undefined) {
      buckets.set(key, [row])
      continue
    }
    bucket.push(row)
  }
  return [...buckets.entries()].map(([key, grouped]) => ({ key, rows: grouped }))
}

function groupKey(row: CarrierInquiry, groupBy: BuyDeskGroupBy): string {
  if (groupBy === "status") {
    return row.status
  }
  if (groupBy === "country") {
    return row.country_code ?? "—"
  }
  if (groupBy === "thread") {
    const origin = row.origin_port_id ?? "—"
    const dest = row.destination_port_id ?? "—"
    return `${origin}|${dest}`
  }
  return row.party_id ?? "—"
}
