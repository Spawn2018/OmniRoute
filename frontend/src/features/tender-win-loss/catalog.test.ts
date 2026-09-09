import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { verdictWrite } from "@/lib/tender-win-losses-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("verdictWrite", () => {
  it("trims win-loss fields without money math", () => {
    expect(
      verdictWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        resultStamp: " lost ",
        whyStamp: " price ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      outcome: "lost",
      reason_code: "price",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_win_loss surface for 176.0", () => {
  it("records an outcome on /tender-win-losses without extract or amount", () => {
    const page = src("features/tender-win-loss/catalog-page.tsx")
    const panel = src("features/tender-win-loss/verdict-form.tsx")
    expect(src("routes/tender-win-losses.tsx")).toContain("/tender-win-losses")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-win-losses"')
    expect(src("lib/business-lists.ts")).toContain("tenderWinLoss")
    expect(page).toContain('data-tender-win-loss="desk"')
    expect(page).toContain("VerdictPanel")
    expect(panel).toContain("persistVerdictMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz wynik")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"176.0": "/tender-win-losses"')
  })
})
