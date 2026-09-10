import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { toSlotWrite } from "@/lib/terminal-slot-connectors-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("toSlotWrite", () => {
  it("trims HITL fields without money math or live T8", () => {
    expect(
      toSlotWrite({
        slotKey: " gdynia_bct ",
        gateToken: " plgdy_bct ",
        regime: " email_hitl ",
        openStamp: "06:00",
        closeStamp: "22:00",
        cutStamp: "16:00",
        originHint: "tenant:manual",
      }),
    ).toEqual({
      connector_code: "gdynia_bct",
      terminal_code: "plgdy_bct",
      mode: "email_hitl",
      opens_local: "06:00",
      closes_local: "22:00",
      cutoff_local: "16:00",
      source_ref: "tenant:manual",
    })
  })
})

describe("terminal_slot_connector surface for 269.0", () => {
  it("records HITL capability and N4 hours without confirm or Money", () => {
    const page = src("features/terminal-slot-connector/catalog-page.tsx")
    const panel = src("features/terminal-slot-connector/terminal-slot-connector-form.tsx")
    expect(src("routes/terminal-slot-connectors.tsx")).toContain("/terminal-slot-connectors")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/terminal-slot-connectors"')
    expect(src("lib/business-lists.ts")).toContain("terminalSlotConnector")
    expect(page).toContain('data-terminal-slot-connector="desk"')
    expect(page).toContain("TerminalSlotConnectorDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistTerminalSlotConnector")
    expect(panel).toContain("Zapisz konektor slotu")
    expect(panel).not.toContain("Potwierdź")
    expect(panel).not.toContain("confirmed")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("parseFloat")
    expect(src("features/ops/ops-index.ts")).toContain('"269.0": "/terminal-slot-connectors"')
  })
})
