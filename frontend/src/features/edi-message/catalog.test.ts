import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("edi message surface for 32.0 and 95.0", () => {
  it("ships /edi without a parser", () => {
    const page = readFileSync(path.join(srcRoot, "features/edi-message/catalog-page.tsx"), "utf8")
    expect(readFileSync(path.join(srcRoot, "routes/edi.tsx"), "utf8")).toContain("/edi")
    expect(readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")).toContain("/edi")
    expect(readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")).toContain("ediMessage")
    expect(readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")).toContain("/edi")
    expect(page).toContain('data-edi-message="board"')
    expect(page).not.toContain("x12")
    expect(page).not.toContain("edifact")
    expect(page).not.toContain("iftmin")
    expect(page).not.toContain("CatalogCreateForm")
  })

  it("records 95.0 as live edi messages on /edi", () => {
    const page = readFileSync(path.join(srcRoot, "features/edi-message/catalog-page.tsx"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/edi-messages-api.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(ops).toContain('"95.0": "/edi"')
    expect(api).toContain("createEdiMessage")
    expect(page).toContain("fetchEdiMessages")
    expect(page).toContain("Zapisz komunikat")
    expect(page).not.toContain("quotationCarrierInquiries")
    expect(page).not.toContain("fetchChannelQuotes")
  })
})
