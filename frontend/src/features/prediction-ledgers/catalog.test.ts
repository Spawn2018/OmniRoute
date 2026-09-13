import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { ledgerWrite } from "@/lib/prediction-ledgers-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("ledgerWrite", () => {
  it("trims ledger fields without money math", () => {
    expect(
      ledgerWrite({
        kindStamp: " eta ",
        horizonStamp: " h24h ",
        lowStamp: " 30 ",
        highStamp: " 90 ",
        modelStamp: " hist_eta ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      prediction_kind: "eta",
      horizon_code: "h24h",
      interval_low: "30",
      interval_high: "90",
      model_code: "hist_eta",
      source_ref: "tenant:manual",
    })
  })
})

describe("prediction_ledger surface for 193.0", () => {
  it("records a scored interval on /prediction-ledgers without Money", () => {
    const page = src("features/prediction-ledgers/catalog-page.tsx")
    const panel = src("features/prediction-ledgers/ledger-form.tsx")
    expect(src("routes/prediction-ledgers.tsx")).toContain("/prediction-ledgers")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/prediction-ledgers"')
    expect(src("lib/business-lists.ts")).toContain("predictionLedger")
    expect(page).toContain('data-prediction-ledger="desk"')
    expect(page).toContain("LedgerPanel")
    expect(panel).toContain("persistLedgerMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz ledger predykcji")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"193.0": "/prediction-ledgers"')
    expect(src("features/ops/ops-index.ts")).toContain('"446.0": "/prediction-ledgers"')
    expect(panel).not.toContain("aria-label=\"CRPS\"")
    expect(panel).not.toContain("aria-label=\"MAE\"")
  })
})
