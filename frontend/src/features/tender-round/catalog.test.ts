import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { roundWrite } from "@/lib/tender-rounds-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("roundWrite", () => {
  it("parses round number without money math", () => {
    expect(
      roundWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        turnStamp: " 2 ",
        originRef: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      round_no: 2,
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_round surface for 172.0", () => {
  it("records round number on /tender-rounds without auto-award", () => {
    const page = src("features/tender-round/catalog-page.tsx")
    const panel = src("features/tender-round/round-form.tsx")
    expect(src("routes/tender-rounds.tsx")).toContain("/tender-rounds")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-rounds"')
    expect(src("lib/business-lists.ts")).toContain("tenderRound")
    expect(page).toContain('data-tender-round="desk"')
    expect(page).toContain("RoundPanel")
    expect(panel).toContain("persistRoundMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz rundę")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"172.0": "/tender-rounds"')
  })
})
