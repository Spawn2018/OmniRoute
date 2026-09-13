import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeBenefitLedgerPayload } from "@/lib/benefit-ledgers-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeBenefitLedgerPayload", () => {
  it("trims ledger fields without money math", () => {
    expect(
      makeBenefitLedgerPayload({
        benefitCode: " dock_save ",
        methodLabel: " porownanie z wczorajszym charge ",
        hoursSaved: " 2.5 ",
        savedAmount: " 150 ",
        savedCurrency: " EUR ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      benefit_code: "dock_save",
      method_label: "porownanie z wczorajszym charge",
      hours_saved: "2.5",
      saved_amount: "150",
      saved_currency: "EUR",
      source_ref: "tenant:manual",
    })
  })
})

describe("benefit_ledger surface for 435.0", () => {
  it("records a ledger on /benefit-ledgers with Money", () => {
    const page = src("features/benefit-ledger/catalog-page.tsx")
    const panel = src("features/benefit-ledger/ledger-form.tsx")
    expect(src("routes/benefit-ledgers.tsx")).toContain("/benefit-ledgers")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/benefit-ledgers"')
    expect(src("lib/business-lists.ts")).toContain("benefitLedger")
    expect(page).toContain('data-benefit-ledger="desk"')
    expect(page).toContain("BenefitLedgerComposer")
    expect(page).toContain("<Money")
    expect(panel).toContain("createBenefitLedger")
    expect(panel).toContain("Zapisz ledger oszczędności")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"435.0": "/benefit-ledgers"')
  })
})
