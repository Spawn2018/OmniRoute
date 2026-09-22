import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { channelQuoteCreateBody } from "@/lib/channel-quotes-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("channelQuoteCreateBody", () => {
  it("trims identifiers and uppercases currency without sending source_ref", () => {
    expect(
      channelQuoteCreateBody({
        partyId: "  party-1  ",
        originPortId: "  pol-1  ",
        destinationPortId: "  pod-1  ",
        quoteDate: "2026-09-01",
        amount: " 1200.0000 ",
        currency: " usd ",
        transportMode: "other",
      }),
    ).toEqual({
      party_id: "party-1",
      origin_port_id: "pol-1",
      destination_port_id: "pod-1",
      quote_date: "2026-09-01",
      amount: "1200.0000",
      currency: "USD",
      transport_mode: "other",
    })
  })

  it("defaults blank transport mode to other", () => {
    expect(
      channelQuoteCreateBody({
        partyId: "p",
        originPortId: "o",
        destinationPortId: "d",
        quoteDate: "2026-09-01",
        amount: "1",
        currency: "PLN",
        transportMode: "  ",
      }).transport_mode,
    ).toBe("other")
  })
})

describe("channel-quotes catalog surface for 13.0 / 620.0", () => {
  it("ships quote table with amount, resolve, transport_mode and no live IATA", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/channel-quotes/catalog-page.tsx"),
      "utf8",
    )
    const route = readFileSync(path.join(srcRoot, "routes/channel-quotes.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/channel-quotes")
    expect(nav).toContain("/channel-quotes")
    expect(lists).toContain("channelQuotes")
    expect(ops).toContain("/channel-quotes")
    expect(ops).toContain('"620.0": "/channel-quotes"')
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("createChannelQuote")
    expect(page).toContain("resolveChannelQuote")
    expect(page).toContain("source_ref")
    expect(page).toContain("amount")
    expect(page).toContain("transportMode")
    expect(page).toContain("transport_mode")
    expect(page).toContain("<Money")
    expect(page.includes("CatalogCreateForm")).toBe(false)
    expect(page.includes("charge.margin")).toBe(false)
    expect(page.includes("fetch(")).toBe(false)
    expect(page.includes("maersk")).toBe(false)
    expect(page.includes("iata")).toBe(false)
  })
})
