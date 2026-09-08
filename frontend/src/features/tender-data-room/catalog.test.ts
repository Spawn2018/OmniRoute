import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { ndaWrite } from "@/lib/tender-data-rooms-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("ndaWrite", () => {
  it("trims NDA mark without money math", () => {
    expect(
      ndaWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        ndaStamp: " signed ",
        originRef: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      nda_mark: "signed",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_data_room surface for 173.0", () => {
  it("records NDA on /tender-data-rooms without extract or amount", () => {
    const page = src("features/tender-data-room/catalog-page.tsx")
    const panel = src("features/tender-data-room/room-form.tsx")
    expect(src("routes/tender-data-rooms.tsx")).toContain("/tender-data-rooms")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-data-rooms"')
    expect(src("lib/business-lists.ts")).toContain("tenderDataRoom")
    expect(page).toContain('data-tender-data-room="desk"')
    expect(page).toContain("RoomPanel")
    expect(panel).toContain("persistRoomMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz pokój")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"173.0": "/tender-data-rooms"')
  })
})
