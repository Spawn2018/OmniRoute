import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { kreptdWrite } from "@/lib/kreptd-licences-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("kreptdWrite", () => {
  it("trims KREPTD licence fields without money math", () => {
    expect(
      kreptdWrite({
        partyStamp: " 11111111-1111-1111-1111-111111111111 ",
        licenceStamp: " GITD-12345678 ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      party_id: "11111111-1111-1111-1111-111111111111",
      licence_no: "GITD-12345678",
      source_ref: "tenant:manual",
    })
  })
})

describe("kreptd_licence surface for 186.0", () => {
  it("records a KREPTD number on /kreptd-licences without scrape or amount", () => {
    const page = src("features/kreptd-licence/catalog-page.tsx")
    const panel = src("features/kreptd-licence/licence-form.tsx")
    expect(src("routes/kreptd-licences.tsx")).toContain("/kreptd-licences")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/kreptd-licences"')
    expect(src("lib/business-lists.ts")).toContain("kreptdLicence")
    expect(page).toContain('data-kreptd-licence="desk"')
    expect(page).toContain("KreptdPanel")
    expect(panel).toContain("persistKreptdMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz licencję KREPTD")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"186.0": "/kreptd-licences"')
  })
})
