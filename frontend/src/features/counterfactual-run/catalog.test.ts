import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeCounterfactualRunPayload } from "@/lib/counterfactual-runs-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeCounterfactualRunPayload", () => {
  it("trims run fields without money math", () => {
    expect(
      makeCounterfactualRunPayload({
        runCode: " fuel_spike ",
        snapshotId: " 11111111-1111-1111-1111-111111111111 ",
        baselineLabel: " plan z wczoraj ",
        leversLabel: " paliwo w gore ",
        resultLabel: " eta plus dwie godziny ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      run_code: "fuel_spike",
      plan_snapshot_id: "11111111-1111-1111-1111-111111111111",
      baseline_label: "plan z wczoraj",
      levers_label: "paliwo w gore",
      result_label: "eta plus dwie godziny",
      source_ref: "tenant:manual",
    })
  })
})

describe("counterfactual_run surface for 453.0", () => {
  it("records a run bound to an existing snapshot", () => {
    const page = src("features/counterfactual-run/catalog-page.tsx")
    const panel = src("features/counterfactual-run/ledger-form.tsx")
    expect(src("routes/counterfactual-runs.tsx")).toContain("/counterfactual-runs")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/counterfactual-runs"')
    expect(src("lib/business-lists.ts")).toContain("counterfactualRun")
    expect(page).toContain('data-counterfactual-run="desk"')
    expect(page).toContain("CounterfactualRunComposer")
    expect(page).toContain("loadWhatIfReplays")
    expect(page).toContain("powtórka nie liczy")
    expect(panel).toContain("createCounterfactualRun")
    expect(panel).toContain("musi istniec")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz przebieg what-if")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"434.0": "/counterfactual-runs"')
    expect(src("features/ops/ops-index.ts")).toContain('"453.0": "/counterfactual-runs"')
  })
})
