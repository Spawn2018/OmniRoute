import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { clockWrite } from "@/lib/free-time-clocks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("clockWrite", () => {
  it("trims kind and origin and parses free days without money math", () => {
    expect(
      clockWrite({
        kindStamp: " detention ",
        daysStamp: " 7 ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      clock_kind: "detention",
      free_days: 7,
      source_ref: "tenant:manual",
    })
  })
})

describe("free_time_clock surface for 196.0", () => {
  it("records a HITL clock on /free-time-clocks without Money or countdown", () => {
    const page = src("features/free-time-clock/catalog-page.tsx")
    const panel = src("features/free-time-clock/clock-form.tsx")
    expect(src("routes/free-time-clocks.tsx")).toContain("/free-time-clocks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/free-time-clocks"')
    expect(src("lib/business-lists.ts")).toContain("freeTimeClock")
    expect(page).toContain('data-free-time-clock="desk"')
    expect(page).toContain("ClockPanel")
    expect(panel).toContain("persistClockMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz zegar D")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("gate_in")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"196.0": "/free-time-clocks"')
  })
})
