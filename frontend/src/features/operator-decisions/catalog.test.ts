import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { operatorDecisionCreateBody } from "@/lib/operator-decisions-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("operatorDecisionCreateBody", () => {
  it("fixes kind to inbound_message and trims ids", () => {
    expect(
      operatorDecisionCreateBody({
        subjectId: " 11111111-1111-1111-1111-111111111111 ",
        sourceRef: " fixture://operator-decision/1 ",
      }),
    ).toEqual({
      subject_kind: "inbound_message",
      subject_id: "11111111-1111-1111-1111-111111111111",
      source_ref: "fixture://operator-decision/1",
    })
  })
})

describe("operator decisions catalog surface for 74.0", () => {
  it("ships /decisions with create and accept/reject", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/operator-decisions/catalog-page.tsx"),
      "utf8",
    )
    const route = readFileSync(path.join(srcRoot, "routes/decisions.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    const buttons = readFileSync(
      path.join(srcRoot, "features/operator-decisions/decide-status-buttons.tsx"),
      "utf8",
    )
    expect(route).toContain("/decisions")
    expect(nav).toContain("/decisions")
    expect(lists).toContain("operatorDecisions")
    expect(ops).toContain("/decisions")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("createOperatorDecision")
    expect(page).toContain("decideOperatorDecision")
    expect(page).toContain("DecideStatusButtons")
    expect(page).toContain("Akceptuj")
    expect(buttons).toContain("Zmień")
    expect(buttons).toContain("Odrzuć")
    expect(page).toContain("lock_version")
    expect(page).not.toContain("amount")
    expect(page).not.toContain("ExtractionService")
  })

  it("ships changed as a locked decide verdict on /decisions", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/operator-decisions/catalog-page.tsx"),
      "utf8",
    )
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/operator-decisions-api.ts"), "utf8")
    expect(ops).toContain('"121.0": "/decisions"')
    expect(page).toContain("DecideStatusButtons")
    expect(api).toContain("OperatorDecideStatus")
    expect(api).toContain("changed")
    expect(page).not.toContain("acceptExtraction")
    expect(page).not.toContain("parseFloat")
  })
})
