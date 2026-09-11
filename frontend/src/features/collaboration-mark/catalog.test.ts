import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { toCollaborationWrite } from "@/lib/collaboration-marks-api"

const src = (rel: string) =>
  readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("toCollaborationWrite", () => {
  it("normalizes slug and role", () => {
    expect(
      toCollaborationWrite({
        slug: " seat_carrier_01 ",
        role: " Carrier ",
        pointer: "tenant:manual",
      }),
    ).toEqual({
      mark_code: "seat_carrier_01",
      role_kind: "carrier",
      source_ref: "tenant:manual",
    })
  })
})

describe("collaboration_mark surface for 284.0", () => {
  it("ships HITL role catalog without shared select", () => {
    const board = src("features/collaboration-mark/catalog-page.tsx")
    const editor = src("features/collaboration-mark/collaboration-mark-form.tsx")
    const client = src("lib/collaboration-marks-api.ts")
    expect(src("routes/collaboration-marks.tsx")).toContain("/collaboration-marks")
    expect(src("components/layout/sidebar.tsx")).toContain(
      'to: "/collaboration-marks"',
    )
    expect(src("lib/business-lists.ts")).toContain("collaborationMark")
    expect(board).toContain("CollaborationMarkBoard")
    expect(editor).toContain("createCollaborationMark")
    expect(editor).not.toContain("shipment_id")
    expect(client).not.toContain("margin")
    expect(src("features/ops/ops-index.ts")).toContain(
      '"284.0": "/collaboration-marks"',
    )
  })
})
