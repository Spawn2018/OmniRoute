import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { toMatchWrite } from "@/lib/routing-guide-matches-api"

const src = (rel: string) =>
  readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("toMatchWrite", () => {
  it("normalizes slug and kind", () => {
    expect(
      toMatchWrite({
        slug: " match_mode_01 ",
        kind: " Mode_Label ",
        pointer: "tenant:manual",
      }),
    ).toEqual({
      mark_code: "match_mode_01",
      match_kind: "mode_label",
      source_ref: "tenant:manual",
    })
  })
})

describe("routing_guide_match surface for 288.0", () => {
  it("ships HITL catalog without matching engine", () => {
    const board = src("features/routing-guide-match/catalog-page.tsx")
    const editor = src("features/routing-guide-match/match-form.tsx")
    const client = src("lib/routing-guide-matches-api.ts")
    expect(src("routes/routing-guide-matches.tsx")).toContain(
      "/routing-guide-matches",
    )
    expect(src("components/layout/sidebar.tsx")).toContain(
      'to: "/routing-guide-matches"',
    )
    expect(src("lib/business-lists.ts")).toContain("routingGuideMatch")
    expect(board).toContain("MatchKindBoard")
    expect(editor).toContain("createRoutingGuideMatch")
    expect(editor).not.toContain("assert_asn")
    expect(client).not.toContain("margin")
    expect(src("features/ops/ops-index.ts")).toContain(
      '"288.0": "/routing-guide-matches"',
    )
  })
})
