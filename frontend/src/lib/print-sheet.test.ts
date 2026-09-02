import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const css = readFileSync(new URL("../index.css", import.meta.url), "utf8")
const packageJson = readFileSync(new URL("../../package.json", import.meta.url), "utf8")

describe("print_sheet for 57.0", () => {
  it("hides shell chrome in print and keeps document boards", () => {
    const printBlock = css.slice(css.indexOf("@media print"))
    expect(printBlock.length).toBeGreaterThan(0)
    expect(printBlock).toContain("aside")
    expect(printBlock).toContain("header")
    expect(printBlock).toContain("display: none")
    expect(printBlock).not.toContain("data-offer-document")
    expect(printBlock).not.toContain("data-sales-invoice")
    expect(printBlock).not.toContain("data-shipment-document")
    expect(packageJson.toLowerCase()).not.toContain("jspdf")
    expect(packageJson).not.toContain("pdf-lib")
  })
})
