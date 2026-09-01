import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { scorecardUpsertBody } from "@/lib/party-scorecards-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("scorecardUpsertBody", () => {
  it("turns blank KPI fields into null and keeps counts", () => {
    expect(
      scorecardUpsertBody({
        partyId: " ignored ",
        responseRate: " 0.8 ",
        medianHours: "  ",
        pricePosition: "0.4",
        quoteInvoiceMatch: "",
        rolloverCount: "2",
        sampleSize: "3",
        windowDays: "60",
      }),
    ).toEqual({
      response_rate: "0.8",
      median_response_hours: null,
      price_position: "0.4",
      quote_invoice_match_rate: null,
      rollover_count: 2,
      sample_size: 3,
      window_days: 60,
    })
  })
})

describe("party-scorecards catalog surface for 10.0", () => {
  it("ships ranking table with snapshot save and no money engine", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/party-scorecards/catalog-page.tsx"),
      "utf8",
    )
    const route = readFileSync(path.join(srcRoot, "routes/party-scorecards.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/party-scorecards")
    expect(nav).toContain("/party-scorecards")
    expect(lists).toContain("partyScorecards")
    expect(ops).toContain("/party-scorecards")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("upsertPartyScorecard")
    expect(page).toContain("source_ref")
    expect(page).not.toContain("amount")
    expect(page).not.toContain("natural_person")
    expect(page).not.toContain("charge.margin")
  })
})
