import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { roomWrite } from "@/lib/war-room-marks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("roomWrite", () => {
  it("trims incident without money math or chat", () => {
    expect(roomWrite({ kindStamp: " labor ", originStamp: "tenant:manual" })).toEqual({
      incident_kind: "labor",
      source_ref: "tenant:manual",
    })
  })
})

describe("war_room_mark surface for 200.0", () => {
  it("records a HITL incident on /war-room-marks without Money or coalescence", () => {
    const page = src("features/war-room-mark/catalog-page.tsx")
    const panel = src("features/war-room-mark/room-form.tsx")
    expect(src("routes/war-room-marks.tsx")).toContain("/war-room-marks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/war-room-marks"')
    expect(src("lib/business-lists.ts")).toContain("warRoomMark")
    expect(page).toContain('data-war-room="desk"')
    expect(page).toContain("RoomPanel")
    expect(panel).toContain("persistRoomMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz salę kryzysową")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"200.0": "/war-room-marks"')
  })
})
