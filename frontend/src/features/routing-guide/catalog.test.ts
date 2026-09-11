import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { routingGuideBody } from "@/lib/routing-guides-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("routingGuideBody", () => {
  it("trims HITL fields and turns blank labels into null", () => {
    expect(
      routingGuideBody({
        guideSlug: " guide_pl_de ",
        laneText: " Gdańsk–Hamburg ",
        modeText: "  ",
        originPointer: "tenant:manual",
      }),
    ).toEqual({
      guide_code: "guide_pl_de",
      lane_label: "Gdańsk–Hamburg",
      mode_label: null,
      source_ref: "tenant:manual",
    })
  })
})

describe("routing_guide surface for 279.0", () => {
  it("records HITL guide on /routing-guides without 409 or money", () => {
    const page = src("features/routing-guide/catalog-page.tsx")
    const panel = src("features/routing-guide/routing-guide-form.tsx")
    const client = src("lib/routing-guides-api.ts")
    expect(src("routes/routing-guides.tsx")).toContain("/routing-guides")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/routing-guides"')
    expect(src("lib/business-lists.ts")).toContain("routingGuide")
    expect(page).toContain('data-routing-guide="board"')
    expect(page).toContain("RoutingGuideDesk")
    expect(panel).toContain("persistRoutingGuide")
    expect(panel).toContain("Zapisz przewodnik routingu")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("Blokuj zlecenie")
    expect(client).not.toContain("shipment_id")
    expect(client).not.toContain("blocks_dispatch")
    expect(src("features/ops/ops-index.ts")).toContain('"279.0": "/routing-guides"')
  })
})
