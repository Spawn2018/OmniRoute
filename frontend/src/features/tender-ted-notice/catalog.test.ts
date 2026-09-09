import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { tedWrite } from "@/lib/tender-ted-notices-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("tedWrite", () => {
  it("trims TED notice fields without money math", () => {
    expect(
      tedWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        noticeStamp: " 123456-2024 ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      notice_number: "123456-2024",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_ted_notice surface for 183.0", () => {
  it("records a TED number on /tender-ted-notices without scrape or amount", () => {
    const page = src("features/tender-ted-notice/catalog-page.tsx")
    const panel = src("features/tender-ted-notice/notice-form.tsx")
    expect(src("routes/tender-ted-notices.tsx")).toContain("/tender-ted-notices")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-ted-notices"')
    expect(src("lib/business-lists.ts")).toContain("tenderTedNotice")
    expect(page).toContain('data-tender-ted-notice="desk"')
    expect(page).toContain("TedPanel")
    expect(panel).toContain("persistTedMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz ogłoszenie TED")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"183.0": "/tender-ted-notices"')
  })
})
