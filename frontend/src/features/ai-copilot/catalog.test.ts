import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { aiProposals } from "@/lib/extractions-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("aiProposals", () => {
  it("keeps pending drafts and drops accepted", () => {
    expect(
      aiProposals([
        { status: "accepted" },
        { status: "pending" },
      ]),
    ).toEqual([{ status: "pending" }])
  })
})

describe("ai copilot surface for 47.0", () => {
  it("ships /ai as pending drafts without a chat table", () => {
    const page = src("features/ai-copilot/catalog-page.tsx")
    expect(src("routes/ai.tsx")).toContain("/ai")
    expect(src("components/layout/sidebar.tsx")).toContain("/ai")
    expect(src("lib/business-lists.ts")).toContain("aiCopilot")
    expect(src("features/ops/ops-index.ts")).toContain("/ai")
    expect(page).toContain('data-ai-copilot="board"')
    expect(page).toContain("aiProposals")
    expect(page).toContain("fetchExtractionDrafts")
    expect(page).toContain("source_ref")
    expect(page).not.toContain("input_text")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("acceptExtraction")
  })

  it("ships stored mail_draft beside extract on the same /ai screen", () => {
    const page = src("features/ai-copilot/catalog-page.tsx")
    const api = src("lib/mail-drafts-api.ts")
    expect(api).toContain("/api/v1/mail-drafts")
    expect(api).toContain('subject_kind: "mail_draft"')
    expect(page).toContain("createMailDraft")
    expect(page).toContain("Zgłoś do decyzji")
    expect(page).toContain("/decisions")
    expect(page).not.toContain("amount +")
    expect(page).not.toContain("acceptExtraction")
  })
})
