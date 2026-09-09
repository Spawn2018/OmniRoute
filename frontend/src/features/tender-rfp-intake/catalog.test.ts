import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { intakeWrite } from "@/lib/tender-rfp-intakes-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("intakeWrite", () => {
  it("trims RFP intake fields without money math", () => {
    expect(
      intakeWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        codeStamp: " scope ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      intake_code: "scope",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_rfp_intake surface for 178.0", () => {
  it("records an RFP intake on /tender-rfp-intakes without extract write or amount", () => {
    const page = src("features/tender-rfp-intake/catalog-page.tsx")
    const panel = src("features/tender-rfp-intake/intake-form.tsx")
    expect(src("routes/tender-rfp-intakes.tsx")).toContain("/tender-rfp-intakes")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-rfp-intakes"')
    expect(src("lib/business-lists.ts")).toContain("tenderRfpIntake")
    expect(page).toContain('data-tender-rfp-intake="desk"')
    expect(page).toContain("IntakePanel")
    expect(panel).toContain("persistIntakeMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz przyjęcie")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"178.0": "/tender-rfp-intakes"')
  })
})
