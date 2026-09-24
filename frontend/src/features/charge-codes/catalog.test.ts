import { describe, expect, it } from "vitest"
import { chargeCodeCreateBody } from "@/lib/charge-codes-api"

describe("chargeCodeCreateBody", () => {
  it("splits aliases on comma and drops blanks", () => {
    expect(
      chargeCodeCreateBody({
        code: " baf ",
        name: " Bunker ",
        aliasesText: " bunker , , BAF_ADJ ",
        sourceRef: " tenant:manual ",
      }),
    ).toEqual({
      code: "baf",
      name: "Bunker",
      aliases: ["bunker", "BAF_ADJ"],
      source_ref: "tenant:manual",
    })
  })

  it("sends empty aliases when the field is blank", () => {
    expect(
      chargeCodeCreateBody({
        code: "WAITING",
        name: "Waiting time",
        aliasesText: "",
        sourceRef: "fixture://charge-code/waiting",
      }),
    ).toEqual({
      code: "WAITING",
      name: "Waiting time",
      aliases: [],
      source_ref: "fixture://charge-code/waiting",
    })
  })
})
