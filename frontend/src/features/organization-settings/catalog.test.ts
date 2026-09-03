import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { organizationSettingUpsertBody } from "@/lib/organization-settings-api"

describe("organizationSettingUpsertBody", () => {
  it("sends allowlisted key and text value", () => {
    expect(
      organizationSettingUpsertBody({
        settingKey: " default_currency ",
        settingValue: " eur ",
      }),
    ).toEqual({
      setting_key: "default_currency",
      setting_value: "eur",
    })
  })

  it("sends prefix and template keys without inventing a number", () => {
    expect(
      organizationSettingUpsertBody({
        settingKey: " quotation_number_prefix ",
        settingValue: " or-q ",
      }),
    ).toEqual({
      setting_key: "quotation_number_prefix",
      setting_value: "or-q",
    })
    expect(
      organizationSettingUpsertBody({
        settingKey: "quotation_print_template",
        settingValue: " letter ",
      }).setting_value,
    ).toBe("letter")
  })
})

describe("organization settings catalog screen", () => {
  it("offers prefix and template save on the same settings page", () => {
    const page = readFileSync(new URL("./catalog-page.tsx", import.meta.url), "utf8")
    expect(page).toContain("quotation_number_prefix")
    expect(page).toContain("quotation_print_template")
    expect(page).toContain("Prefiks numeru oferty")
    expect(page).toContain("Szablon oferty")
    expect(page).not.toContain("document_number")
  })
})
