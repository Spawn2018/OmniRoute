import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { createElement } from "react"
import { renderToStaticMarkup } from "react-dom/server"
import { describe, expect, it } from "vitest"
import { SkipToMain } from "@/components/skip-to-main"
import { HitlReviewSplit } from "@/features/extraction/hitl-review-split"
import {
  MAIN_CONTENT_ID,
  OPERATOR_KEYBOARD_PATH,
  SKIP_TO_MAIN_LABEL,
} from "@/lib/a11y"
import type { ExtractionDraft } from "@/lib/extractions-api"

const css = readFileSync(
  path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../index.css"),
  "utf8",
)

function sampleDraft(): ExtractionDraft {
  return {
    id: "11111111-1111-1111-1111-111111111111",
    organization_id: "22222222-2222-2222-2222-222222222222",
    status: "pending",
    source_ref: "doc://tariff",
    input_text: "THC 100 EUR",
    payload: {
      source_ref: "doc://tariff",
      unparsed_regions: [],
      candidates: [{ code: "THC", amount_text: "100", currency: "EUR" }],
    },
    reviewed_by: null,
    reviewed_at: null,
  }
}

describe("operator keyboard path", () => {
  it("requires a global focus-visible rule, not only RTL", () => {
    expect(css).toContain(":focus-visible")
    expect(css).toContain("outline: 2px solid var(--ring)")
  })

  it("ships the Wyceny/Zlecenia banner shade transition", () => {
    expect(css).toContain("--banner-from: oklch(0.32 0.06 165)")
    expect(css).toContain("--banner-to: oklch(0.42 0.1 165)")
    expect(css).toContain("linear-gradient(120deg, var(--banner-from), var(--banner-to))")
  })

  it("ships oklch tokens and a dark theme instead of hex-only :root", () => {
    const root = css.slice(css.indexOf(":root"), css.indexOf("@theme"))
    expect(css).toContain("oklch(")
    expect(css).toContain(".dark")
    expect(root).not.toMatch(
      /--(background|foreground|card|muted-foreground|primary):\s*#/,
    )
  })

  it("exposes skip-to-main and HITL accept in the keyboard path", () => {
    const skip = renderToStaticMarkup(createElement(SkipToMain))
    expect(skip).toContain(SKIP_TO_MAIN_LABEL)
    expect(skip).toContain(`#${MAIN_CONTENT_ID}`)

    const hitl = renderToStaticMarkup(
      createElement(HitlReviewSplit, {
        draft: sampleDraft(),
        pdfBase64: null,
        busy: false,
        onAccept: () => undefined,
        onReject: () => undefined,
      }),
    )
    expect(hitl).toContain("data-operator-target=\"accept\"")
    expect(hitl).toContain("Akceptuj")
    expect(hitl).toContain("Odrzuć")
    expect(hitl).toContain("<button")

    const ids = OPERATOR_KEYBOARD_PATH.map((step) => step.id)
    expect(ids).toEqual([
      "skip-main",
      "command-palette",
      "extract",
      "hitl-accept",
      "hitl-reject",
      "density",
    ])
  })
})
