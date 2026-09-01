import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("partyCreateBody", () => {
  it("trims legal name, folds country and tax id, splits roles", async () => {
    const { partyCreateBody } = await import("@/lib/parties-api")
    expect(
      partyCreateBody({
        legalName: " ACME Sp. z o.o. ",
        countryCode: " pl ",
        taxId: " 123-456-32-18 ",
        rolesText: " customer , vendor ",
      }),
    ).toEqual({
      legal_name: "ACME Sp. z o.o.",
      country_code: "PL",
      tax_id: "1234563218",
      roles: ["customer", "vendor"],
    })
  })
})

describe("parties catalog surface for 5.0", () => {
  it("ships /parties on DataTableShell with create, resolve, lookup and dependent panels", () => {
    const page = readFileSync(path.join(srcRoot, "features/parties/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/parties.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/parties")
    expect(nav).toContain("/parties")
    expect(lists).toContain("parties")
    expect(ops).toContain("/parties")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("createParty")
    expect(page).toContain("resolveParty")
    expect(page).toContain("resolvePartyEmail")
    expect(page).toContain("Sprawdź mail")
    expect(page).toContain("lookupParty")
    expect(page).toContain("contacts")
    expect(page).toContain("bank")
    expect(page).toContain("email-domain")
    expect(page).toContain("carrier")
    expect(page).toContain("charge-override")
    expect(page).toContain("<Money")
  })

  it("terminals picker ships operator_party_id while operator_name still saves", () => {
    const api = readFileSync(path.join(srcRoot, "lib/terminals-api.ts"), "utf8")
    const page = readFileSync(path.join(srcRoot, "features/geography/terminals-page.tsx"), "utf8")
    expect(api).toContain("operator_party_id")
    expect(api).toContain("operator_name")
    expect(page).toContain("operator_party_id")
    expect(page).toContain("operator_name")
    expect(page).toContain("fetchParties")
  })
})
