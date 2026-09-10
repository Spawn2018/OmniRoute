import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { snapshotWrite } from "@/lib/plan-snapshots-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("snapshotWrite", () => {
  it("trims HITL fields without money math or km", () => {
    expect(
      snapshotWrite({
        codeStamp: " plan_v1 ",
        shipmentStamp: " 11111111-1111-4111-8111-111111111111 ",
        tripStamp: " 22222222-2222-4222-8222-222222222222 ",
        resourceStamp: " 33333333-3333-4333-8333-333333333333 ",
        authorStamp: " Anna ",
        whenStamp: " 2026-09-10T12:00:00+02:00 ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      snapshot_code: "plan_v1",
      shipment_id: "11111111-1111-4111-8111-111111111111",
      trip_id: "22222222-2222-4222-8222-222222222222",
      resource_id: "33333333-3333-4333-8333-333333333333",
      author_label: "Anna",
      recorded_at: "2026-09-10T12:00:00+02:00",
      source_ref: "tenant:manual",
    })
  })
})

describe("plan_snapshot surface for 265.0", () => {
  it("records a HITL snapshot on /plan-snapshots without Money or map", () => {
    const page = src("features/plan-snapshot/catalog-page.tsx")
    const panel = src("features/plan-snapshot/snapshot-form.tsx")
    expect(src("routes/plan-snapshots.tsx")).toContain("/plan-snapshots")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/plan-snapshots"')
    expect(src("lib/business-lists.ts")).toContain("planSnapshot")
    expect(page).toContain('data-plan-snapshot="desk"')
    expect(page).toContain("SnapshotDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistSnapshot")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz migawkę")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"265.0": "/plan-snapshots"')
  })
})
