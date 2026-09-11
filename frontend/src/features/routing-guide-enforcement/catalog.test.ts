import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { packEnforcementMode } from "@/lib/routing-guide-enforcements-api"

const src = (rel: string) =>
  readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("packEnforcementMode", () => {
  it("trims code and lowercases mode", () => {
    expect(
      packEnforcementMode({
        code: " mode_block_01 ",
        mode: " Block_409 ",
        origin: "tenant:manual",
      }),
    ).toEqual({
      mark_code: "mode_block_01",
      enforcement_kind: "block_409",
      source_ref: "tenant:manual",
    })
  })
})

describe("routing_guide_enforcement surface for 285.0", () => {
  it("ships HITL enforcement catalog without live 409", () => {
    const desk = src("features/routing-guide-enforcement/enforcement-mode-desk.tsx")
    const composer = src(
      "features/routing-guide-enforcement/enforcement-mode-composer.tsx",
    )
    const client = src("lib/routing-guide-enforcements-api.ts")
    expect(src("routes/routing-guide-enforcements.tsx")).toContain(
      "/routing-guide-enforcements",
    )
    expect(src("components/layout/sidebar.tsx")).toContain(
      'to: "/routing-guide-enforcements"',
    )
    expect(src("lib/business-lists.ts")).toContain("routingGuideEnforcement")
    expect(desk).toContain("EnforcementModeDesk")
    expect(composer).toContain("postEnforcementMode")
    expect(composer).toContain("aria-pressed")
    expect(composer).not.toContain("shipment_id")
    expect(client).not.toContain("margin")
    expect(src("features/ops/ops-index.ts")).toContain(
      '"285.0": "/routing-guide-enforcements"',
    )
  })
})
