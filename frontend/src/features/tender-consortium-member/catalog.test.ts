import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { seatWrite } from "@/lib/tender-consortium-members-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("seatWrite", () => {
  it("trims consortium seat fields without money math", () => {
    expect(
      seatWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        partyStamp: " 22222222-2222-2222-2222-222222222222 ",
        chairStamp: " member ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      party_id: "22222222-2222-2222-2222-222222222222",
      seat_code: "member",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_consortium_member surface for 177.0", () => {
  it("records a consortium seat on /tender-consortium-members without extract or amount", () => {
    const page = src("features/tender-consortium-member/catalog-page.tsx")
    const panel = src("features/tender-consortium-member/seat-form.tsx")
    expect(src("routes/tender-consortium-members.tsx")).toContain("/tender-consortium-members")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-consortium-members"')
    expect(src("lib/business-lists.ts")).toContain("tenderConsortiumMember")
    expect(page).toContain('data-tender-consortium-member="desk"')
    expect(page).toContain("SeatPanel")
    expect(panel).toContain("persistSeatMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz fotel")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"177.0": "/tender-consortium-members"')
  })
})
