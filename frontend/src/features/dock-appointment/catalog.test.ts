import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { dockWrite } from "@/lib/dock-appointments-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("dockWrite", () => {
  it("trims appointment fields without parsing money", () => {
    expect(
      dockWrite({
        orderKey: "  ship  ",
        haltRef: " halt ",
        slotToken: "dock_1",
        stageMark: "advised",
        dayMark: "2026-09-09",
        openMark: "08:00",
        closeMark: "10:00",
        originNote: "tenant:manual",
      }),
    ).toEqual({
      shipment_id: "ship",
      stop_id: "halt",
      appointment_code: "dock_1",
      appointment_status: "advised",
      window_date: "2026-09-09",
      window_start_local: "08:00",
      window_end_local: "10:00",
      source_ref: "tenant:manual",
    })
  })
})

describe("dock_appointment surface for 157.0", () => {
  it("records a warehouse window on /dock-appointments without WMS", () => {
    const page = src("features/dock-appointment/catalog-page.tsx")
    const panel = src("features/dock-appointment/window-form.tsx")
    expect(src("routes/dock-appointments.tsx")).toContain("/dock-appointments")
    expect(src("components/layout/sidebar.tsx")).toContain("/dock-appointments")
    expect(src("lib/business-lists.ts")).toContain("dockAppointment")
    expect(page).toContain('data-dock="desk"')
    expect(page).toContain("DockWindowForm")
    expect(panel).toContain("persistDock")
    expect(panel).toContain('data-dock="window-form"')
    expect(panel).toContain("Zapisz awizację doku")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("wms")
    expect(src("features/ops/ops-index.ts")).toContain('"157.0": "/dock-appointments"')
  })
})
