import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { playWrite } from "@/lib/tender-playbooks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("playWrite", () => {
  it("trims playbook fields without money math", () => {
    expect(
      playWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        thesisStamp: " incoterm_fob ",
        bodyStamp: " tylko FOB ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      claim_code: "incoterm_fob",
      claim_text: "tylko FOB",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_playbook surface for 175.0", () => {
  it("records a claim on /tender-playbooks without extract or amount", () => {
    const page = src("features/tender-playbook/catalog-page.tsx")
    const panel = src("features/tender-playbook/play-form.tsx")
    expect(src("routes/tender-playbooks.tsx")).toContain("/tender-playbooks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-playbooks"')
    expect(src("lib/business-lists.ts")).toContain("tenderPlaybook")
    expect(page).toContain('data-tender-playbook="desk"')
    expect(page).toContain("PlayPanel")
    expect(panel).toContain("persistPlayMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz tezę")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"175.0": "/tender-playbooks"')
  })
})
