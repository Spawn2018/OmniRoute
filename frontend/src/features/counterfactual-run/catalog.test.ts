import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeCounterfactualRunPayload } from "@/lib/counterfactual-runs-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeCounterfactualRunPayload", () => {
  it("trims run fields without money math", () => {
    expect(
      makeCounterfactualRunPayload({
        runCode: " fuel_spike ",
        baselineLabel: " plan z wczoraj ",
        leversLabel: " paliwo w gore ",
        resultLabel: " eta plus dwie godziny ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      run_code: "fuel_spike",
      baseline_label: "plan z wczoraj",
      levers_label: "paliwo w gore",
      result_label: "eta plus dwie godziny",
      source_ref: "tenant:manual",
    })
  })
})

describe("counterfactual_run surface for 434.0", () => {
  it("records a run on /counterfactual-runs without Money", () => {
    const page = src("features/counterfactual-run/catalog-page.tsx")
    const panel = src("features/counterfactual-run/ledger-form.tsx")
    expect(src("routes/counterfactual-runs.tsx")).toContain("/counterfactual-runs")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/counterfactual-runs"')
    expect(src("lib/business-lists.ts")).toContain("counterfactualRun")
    expect(page).toContain('data-counterfactual-run="desk"')
    expect(page).toContain("CounterfactualRunComposer")
    expect(panel).toContain("createCounterfactualRun")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz przebieg what-if")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"434.0": "/counterfactual-runs"')
  })
})
