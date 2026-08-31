import { describe, expect, it } from "vitest"
import { mergeColumnOrder } from "@/components/data-table/types"

describe("mergeColumnOrder", () => {
  it("keeps preferred order and appends missing ids", () => {
    expect(mergeColumnOrder(["id", "email"], ["email", "display_name", "id"])).toEqual([
      "id",
      "email",
      "display_name",
    ])
  })

  it("drops unknown preferred ids", () => {
    expect(mergeColumnOrder(["ghost", "email"], ["email", "id"])).toEqual(["email", "id"])
  })
})
