import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import {
  hitlPreviewSegments,
  hitlPreviewSpans,
  isPdfBase64,
} from "@/features/extraction/hitl-spans"

const reviewSplit = readFileSync(
  path.resolve(path.dirname(fileURLToPath(import.meta.url)), "hitl-review-split.tsx"),
  "utf8",
)

describe("HITL span highlights", () => {
  it("marks candidate tokens in the preview", () => {
    const spans = hitlPreviewSpans("THC 100 EUR\nnote", [
      { code: "THC", amount_text: "100", currency: "EUR" },
    ])
    expect(spans.map((span) => span.text)).toEqual(["THC", "100", "EUR"])
    const segments = hitlPreviewSegments("THC 100 EUR\nnote", spans)
    expect(segments.filter((segment) => segment.highlight).map((segment) => segment.text)).toEqual([
      "THC",
      "100",
      "EUR",
    ])
    expect(segments.some((segment) => segment.text.includes("note") && !segment.highlight)).toBe(
      true,
    )
  })

  it("detects PDF magic and keeps pdf.js off the review module graph", () => {
    expect(isPdfBase64(btoa("%PDF-1.4 rest"))).toBe(true)
    expect(isPdfBase64(btoa("THC 100 EUR"))).toBe(false)
    expect(reviewSplit).toContain("lazy(() => import(")
    expect(reviewSplit).not.toContain("pdfjs-dist")
  })
})
