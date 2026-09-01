import { describe, expect, it } from "vitest"
import { portCreateBody } from "@/lib/ports-api"

describe("portCreateBody", () => {
  it("normalizes the unlocode typed with source spacing", () => {
    expect(
      portCreateBody({
        unlocode: " pl gdy ",
        name: " Gdynia ",
        countryCode: " pl ",
        aliasesText: " Gdingen , , Gdynia Port ",
      }),
    ).toEqual({
      unlocode: "PLGDY",
      name: "Gdynia",
      country_code: "PL",
      aliases: ["Gdingen", "Gdynia Port"],
    })
  })

  it("sends empty aliases when the field is blank", () => {
    expect(
      portCreateBody({ unlocode: "DEHAM", name: "Hamburg", countryCode: "DE", aliasesText: "" }),
    ).toEqual({
      unlocode: "DEHAM",
      name: "Hamburg",
      country_code: "DE",
      aliases: [],
    })
  })
})
