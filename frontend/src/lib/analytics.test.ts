import { describe, expect, it } from "vitest"
import { EXTRACT_ACCEPT_EVENTS, isExtractAcceptEvent } from "@/lib/analytics"

const FORBIDDEN = ["nip", "email", "input_text", "from_address", "body_text"]

describe("UXCL-L1 extract-accept allowlist", () => {
  it("names only extraction_draft job events", () => {
    expect([...EXTRACT_ACCEPT_EVENTS]).toEqual([
      "extraction_draft_created",
      "extraction_draft_accepted",
      "extraction_draft_rejected",
      "extraction_draft_patched",
      "extraction_draft_undone",
    ])
    expect(isExtractAcceptEvent("app_loaded")).toBe(false)
    expect(isExtractAcceptEvent("command_palette_used")).toBe(false)
    expect(isExtractAcceptEvent("extraction_draft_accepted")).toBe(true)
  })

  it("fixture payload has no PII keys", () => {
    const fixture: Record<string, never> = {}
    for (const key of FORBIDDEN) {
      expect(Object.hasOwn(fixture, key)).toBe(false)
    }
    expect(Object.keys(fixture)).toHaveLength(0)
  })
})
