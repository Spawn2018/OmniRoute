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
})
