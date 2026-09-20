import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { groupWrite } from "@/lib/stop-groups-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("groupWrite", () => {
  it("trims stop_group fields without parsing money", () => {
    expect(
      groupWrite({
        shipmentToken: "  ship  ",
        groupCode: "GRP1",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      shipment_id: "ship",
      group_code: "GRP1",
      source_ref: "tenant:manual",
    })
  })
})

describe("stop_group surface for 600.0", () => {
  it("records a group header on /stop-groups without membership", () => {
    const page = src("features/stop-group/catalog-page.tsx")
    const panel = src("features/stop-group/group-panel.tsx")
    const ops = src("features/ops/ops-index.ts")
    expect(src("routes/stop-groups.tsx")).toMatch(/\/stop-groups/)
    expect(src("components/layout/sidebar.tsx")).toMatch(/to: "\/stop-groups"/)
    expect(src("lib/business-lists.ts")).toMatch(/stopGroup:/)
    expect(page).toMatch(/data-stop-group="board"/)
    expect(page).toMatch(/StopGroupPanel/)
    expect(panel).toMatch(/persistStopGroup/)
    expect(panel).toMatch(/data-stop-group="group-form"/)
    expect(panel).toMatch(/Zapisz grupę punktów/)
    expect(/parseFloat|leaflet|CatalogCreateForm|buy_amount/.test(panel)).toBe(false)
    expect(ops).toMatch(/"600\.0": "\/stop-groups"/)
  })
})
