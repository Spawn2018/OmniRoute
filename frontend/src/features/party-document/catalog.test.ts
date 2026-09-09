import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { partyDocWrite } from "@/lib/party-documents-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("partyDocWrite", () => {
  it("trims party document fields without money math", () => {
    expect(
      partyDocWrite({
        partyStamp: " 11111111-1111-1111-1111-111111111111 ",
        kindStamp: " ocp ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      party_id: "11111111-1111-1111-1111-111111111111",
      document_kind: "ocp",
      source_ref: "tenant:manual",
    })
  })
})

describe("party_document surface for 188.0", () => {
  it("records a document kind on /party-documents without 409 or amount", () => {
    const page = src("features/party-document/catalog-page.tsx")
    const panel = src("features/party-document/paper-form.tsx")
    expect(src("routes/party-documents.tsx")).toContain("/party-documents")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/party-documents"')
    expect(src("lib/business-lists.ts")).toContain("partyDocument")
    expect(page).toContain('data-party-document="desk"')
    expect(page).toContain("PartyDocPanel")
    expect(panel).toContain("persistPartyDocMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz dokument kontrahenta")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"188.0": "/party-documents"')
  })
})
