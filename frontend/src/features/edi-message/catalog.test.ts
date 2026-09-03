import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

function frontendFile(rel: string): string {
  return readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../..", rel), "utf8")
}

describe("edi message surface for 32.0 and 95.0", () => {
  it("ships /edi as matching channel quotes without a parser", () => {
    const page = frontendFile("features/edi-message/catalog-page.tsx")
    expect(frontendFile("routes/edi.tsx")).toContain("/edi")
    expect(frontendFile("components/layout/sidebar.tsx")).toContain("/edi")
    expect(frontendFile("lib/business-lists.ts")).toContain("ediMessage")
    expect(frontendFile("features/ops/ops-index.ts")).toContain("/edi")
    expect(page).toContain('data-edi-message="board"')
    expect(page).not.toContain("x12")
    expect(page).not.toContain("edifact")
    expect(page).not.toContain("iftmin")
    expect(page).not.toContain("CatalogCreateForm")
  })

  it("records 95.0 as live edi messages on /edi", () => {
    const page = frontendFile("features/edi-message/catalog-page.tsx")
    const api = frontendFile("lib/edi-messages-api.ts")
    const ops = frontendFile("features/ops/ops-index.ts")
    expect(ops).toContain('"95.0": "/edi"')
    expect(api).toContain("createEdiMessage")
    expect(page).toContain("fetchEdiMessages")
    expect(page).toContain("Zapisz komunikat")
    expect(page).not.toContain("quotationCarrierInquiries")
    expect(page).not.toContain("fetchChannelQuotes")
  })
})
