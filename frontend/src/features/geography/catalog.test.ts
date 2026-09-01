import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { zoneCreateBody, zoneMemberCreateBody } from "@/lib/locations-api"
import { portCreateBody } from "@/lib/ports-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

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

describe("terminalCreateBody", () => {
  it("normalizes the isps code typed with mixed case and blank operator", async () => {
    const { terminalCreateBody } = await import("@/lib/terminals-api")
    expect(
      terminalCreateBody({
        portId: "port-1",
        name: " BCT Gdynia ",
        ispsCode: " plgdy-bct ",
        operatorName: "  ",
      }),
    ).toEqual({
      port_id: "port-1",
      name: "BCT Gdynia",
      isps_code: "PLGDY-BCT",
      operator_name: null,
    })
  })
})

describe("geography catalog surfaces for 4.2", () => {
  it("shows world port index columns as read-only fields on ports", () => {
    const api = readFileSync(path.join(srcRoot, "lib/ports-api.ts"), "utf8")
    const page = readFileSync(path.join(srcRoot, "features/geography/ports-page.tsx"), "utf8")
    expect(api).toContain("wpi_number")
    expect(api).toContain("harbor_size")
    expect(page).toContain("wpi_number")
    expect(page).toContain("harbor_size")
    expect(page).toContain("DataTableShell")
  })

  it("ships /terminals on DataTableShell with create, port filter and isps resolve", () => {
    const page = readFileSync(path.join(srcRoot, "features/geography/terminals-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/terminals.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    expect(route).toContain("/terminals")
    expect(nav).toContain("/terminals")
    expect(lists).toContain("terminals")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("port_id")
    expect(page).toContain("createTerminal")
    expect(page).toContain("resolveTerminal")
  })
})
