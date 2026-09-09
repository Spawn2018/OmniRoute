import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { prospectWrite } from "@/lib/tender-prospects-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("prospectWrite", () => {
  it("trims prospect outreach fields without money math", () => {
    expect(
      prospectWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        partyStamp: " 22222222-2222-2222-2222-222222222222 ",
        outreachStamp: " emailed ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      party_id: "22222222-2222-2222-2222-222222222222",
      outreach_code: "emailed",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_prospect surface for 180.0", () => {
  it("records a prospect mark on /tender-prospects without scrape or amount", () => {
    const page = src("features/tender-prospect/catalog-page.tsx")
    const panel = src("features/tender-prospect/prospect-form.tsx")
    expect(src("routes/tender-prospects.tsx")).toContain("/tender-prospects")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-prospects"')
    expect(src("lib/business-lists.ts")).toContain("tenderProspect")
    expect(page).toContain('data-tender-prospect="desk"')
    expect(page).toContain("ProspectPanel")
    expect(panel).toContain("persistProspectMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz prospekt")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"180.0": "/tender-prospects"')
  })
})
