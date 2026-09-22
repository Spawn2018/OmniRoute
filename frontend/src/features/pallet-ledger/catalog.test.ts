import { readFileSync } from "node:fs"
import { resolve } from "node:path"
import { describe, expect, it } from "vitest"
import { ledgerWrite } from "@/lib/pallet-ledgers-api"

const root = resolve(__dirname, "../..")

function src(rel: string): string {
  return readFileSync(resolve(root, rel), "utf8")
}

describe("pallet_ledger surface for 629.0", () => {
  it("records a signed movement on /pallet-ledgers without money", () => {
    expect(src("routes/pallet-ledgers.tsx")).toContain("/pallet-ledgers")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/pallet-ledgers"')
    expect(src("features/ops/ops-index.ts")).toContain('"629.0": "/pallet-ledgers"')
    const body = ledgerWrite({
      counterpartToken: "00000000-0000-4000-8000-000000000001",
      codeToken: "issue_chep_01",
      kindToken: "chep",
      deltaToken: "-2",
      originStamp: "fixture://pallet-ledger/a",
    })
    expect(body.delta_count).toBe(-2)
    expect(body.pallet_kind).toBe("chep")
  })
})
