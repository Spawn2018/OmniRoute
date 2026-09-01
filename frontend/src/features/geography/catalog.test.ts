import { describe, expect, it } from "vitest"
import { zoneCreateBody, zoneMemberCreateBody } from "@/lib/locations-api"
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

describe("zoneCreateBody", () => {
  it("folds the zone code typed with spacing into an underscore token", () => {
    expect(zoneCreateBody({ code: " trojmiasto strefa ", name: " Trójmiasto " })).toEqual({
      code: "TROJMIASTO_STREFA",
      name: "Trójmiasto",
    })
  })
})

describe("zoneMemberCreateBody", () => {
  it("strips the separators operators type in postal codes", () => {
    expect(
      zoneMemberCreateBody({ countryCode: " pl ", postalFrom: "81-000", postalTo: "81 999" }),
    ).toEqual({
      country_code: "PL",
      postal_from: "81000",
      postal_to: "81999",
    })
  })

  it("keeps alphanumeric british codes in one piece", () => {
    expect(
      zoneMemberCreateBody({ countryCode: "gb", postalFrom: "sw1a 0aa", postalTo: "sw1a 9zz" }),
    ).toEqual({
      country_code: "GB",
      postal_from: "SW1A0AA",
      postal_to: "SW1A9ZZ",
    })
  })
})
