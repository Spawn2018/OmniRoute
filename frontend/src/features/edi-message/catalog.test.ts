import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("edi message surface for 32.0", () => {
  it("ships /edi as read-only matching channel quotes without a parser", () => {
    const page = readFileSync(path.join(srcRoot, "features/edi-message/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/edi.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/edi")
    expect(nav).toContain("/edi")
    expect(lists).toContain("ediMessage")
    expect(ops).toContain("/edi")
    expect(page).toContain('data-edi-message="board"')
    expect(page).toContain("quotationCarrierInquiries")
    expect(page).toContain("fetchChannelQuotes")
    expect(page).not.toContain("x12")
    expect(page).not.toContain("edifact")
    expect(page).not.toContain("iftmin")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
