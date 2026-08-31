import { describe, expect, it } from "vitest"
import { chargeCodeCreateBody } from "@/lib/charge-codes-api"

describe("chargeCodeCreateBody", () => {
  it("splits aliases on comma and drops blanks", () => {
    expect(
      chargeCodeCreateBody({
        code: " baf ",
        name: " Bunker ",
        aliasesText: " bunker , , BAF_ADJ ",
      }),
    ).toEqual({
      code: "baf",
      name: "Bunker",
      aliases: ["bunker", "BAF_ADJ"],
    })
  })

  it("sends empty aliases when the field is blank", () => {
    expect(chargeCodeCreateBody({ code: "THC", name: "Terminal", aliasesText: "" })).toEqual({
      code: "THC",
      name: "Terminal",
      aliases: [],
    })
  })
})
