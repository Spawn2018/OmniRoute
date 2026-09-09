import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { edgeWrite } from "@/lib/memory-edges-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("edgeWrite", () => {
  it("trims edge without money math or retrieval", () => {
    expect(edgeWrite({ linkKind: " follows ", originToken: "tenant:manual" })).toEqual({
      edge_kind: "follows",
      source_ref: "tenant:manual",
    })
  })
})

describe("memory_edge surface for 201.0", () => {
  it("records a HITL edge on /memory-edges without Money or retrieval", () => {
    const page = src("features/memory-edge/catalog-page.tsx")
    const board = src("features/memory-edge/edge-board.tsx")
    expect(src("routes/memory-edges.tsx")).toContain("/memory-edges")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/memory-edges"')
    expect(src("lib/business-lists.ts")).toContain("memoryEdge")
    expect(page).toContain('data-memory-edge="desk"')
    expect(page).toContain("EdgeBoard")
    expect(board).toContain("persistEdgeMark")
    expect(board).not.toContain("<Money")
    expect(board).toContain("Zapisz krawędź pamięci")
    expect(board).not.toContain("parseFloat")
    expect(board).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"201.0": "/memory-edges"')
  })
})
