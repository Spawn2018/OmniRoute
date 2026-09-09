import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { weatherWrite } from "@/lib/weather-observations-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("weatherWrite", () => {
  it("trims weather fields and uppercases the station without money math", () => {
    expect(
      weatherWrite({
        conditionStamp: " rain ",
        stationStamp: " plgdy ",
        observedStamp: " 2026-09-09T12:00:00+00:00 ",
        providerStamp: " hitl ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      condition_code: "rain",
      station_unlocode: "PLGDY",
      observed_at: "2026-09-09T12:00:00+00:00",
      provider_code: "hitl",
      source_ref: "tenant:manual",
    })
  })
})

describe("weather_observation surface for 195.0", () => {
  it("records a HITL mark on /weather-observations without Money or Open-Meteo", () => {
    const page = src("features/weather-observation/catalog-page.tsx")
    const panel = src("features/weather-observation/weather-form.tsx")
    expect(src("routes/weather-observations.tsx")).toContain("/weather-observations")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/weather-observations"')
    expect(src("lib/business-lists.ts")).toContain("weatherObservation")
    expect(page).toContain('data-weather-observation="desk"')
    expect(page).toContain("WeatherPanel")
    expect(panel).toContain("persistWeatherMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz pogodę")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("open-meteo")
    expect(src("features/ops/ops-index.ts")).toContain('"195.0": "/weather-observations"')
  })
})
