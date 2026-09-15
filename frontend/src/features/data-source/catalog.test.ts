import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildDataSourceWrite } from "@/lib/data-sources-api"

describe("data_source catalog", () => {
  it("maps plaster 522.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["522.0"]).toBe("/data-sources")
  })

  it("trims source fields", () => {
    expect(
      buildDataSourceWrite({
        code: " ds_openmeteo_01 ",
        license: " CC-BY-4.0 ",
        rights: " weather read-only ",
        origin: " fixture://data-source/1 ",
      }),
    ).toEqual({
      source_code: "ds_openmeteo_01",
      license_label: "CC-BY-4.0",
      rights_scope: "weather read-only",
      source_ref: "fixture://data-source/1",
    })
  })
})
