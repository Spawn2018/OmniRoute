import type { InboundMessage } from "@/lib/inbound-messages-api"

export const MAIL_GROUP_BY = ["party", "country", "status"] as const

export type MailGroupBy = (typeof MAIL_GROUP_BY)[number]

export const DEFAULT_MAIL_GROUP_BY: MailGroupBy = "party"

export type PartyCountry = {
  id: string
  country_code: string
}

export type MailMessageGroup = {
  key: string
  rows: InboundMessage[]
}

export function mailGroupByOrDefault(raw: string): MailGroupBy {
  const token = raw.trim()
  if (token === "country" || token === "status" || token === "party") {
    return token
  }
  return DEFAULT_MAIL_GROUP_BY
}

export function partyCountryMap(parties: readonly PartyCountry[]): Map<string, string> {
  return new Map(parties.map((row) => [row.id, row.country_code]))
}

export function groupInboundMessages(
  rows: readonly InboundMessage[],
  parties: readonly PartyCountry[],
  groupBy: MailGroupBy,
): MailMessageGroup[] {
  const countries = partyCountryMap(parties)
  const buckets = new Map<string, InboundMessage[]>()
  for (const row of rows) {
    const key = groupKey(row, countries, groupBy)
    const bucket = buckets.get(key)
    if (bucket === undefined) {
      buckets.set(key, [row])
      continue
    }
    bucket.push(row)
  }
  return [...buckets.entries()].map(([key, grouped]) => ({ key, rows: grouped }))
}

function groupKey(
  row: InboundMessage,
  countries: Map<string, string>,
  groupBy: MailGroupBy,
): string {
  if (groupBy === "status") {
    return row.status
  }
  if (groupBy === "country") {
    if (row.party_id === null) {
      return "—"
    }
    return countries.get(row.party_id) ?? "—"
  }
  return row.party_id ?? "—"
}
