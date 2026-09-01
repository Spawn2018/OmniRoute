import { createElement } from "react"
import { renderToStaticMarkup } from "react-dom/server"
import { describe, expect, it } from "vitest"
import { OpsIndex } from "@/features/ops/ops-index-page"
import {
  ADMIN_REF_SURFACES,
  HELLO_DASHBOARD_MARKERS,
  OPS_JOBS,
} from "@/features/ops/ops-index"
import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { REQUIRED_BUSINESS_LIST_ROUTES } from "@/lib/business-lists"

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("admin-ref dense ops surface", () => {
  it("lists real operator jobs and refuses hello-dashboard copy", () => {
    const html = renderToStaticMarkup(
      createElement(OpsIndex, { healthLabel: "ok", healthState: "ok" }),
    )
    expect(ADMIN_REF_SURFACES).toEqual(["sidebar-density", "table-toolbar", "command-actions"])
    for (const job of OPS_JOBS) {
      expect(html).toContain(job.route)
      expect(html).toContain(job.label)
    }
    for (const route of REQUIRED_BUSINESS_LIST_ROUTES) {
      expect(OPS_JOBS.some((job) => job.route === route)).toBe(true)
    }
    for (const marker of HELLO_DASHBOARD_MARKERS) {
      expect(html).not.toContain(marker)
    }
    expect(html).toContain('data-admin-ref="ops-index"')
    expect(readFileSync(path.join(root, "components/layout/sidebar.tsx"), "utf8")).toContain(
      'data-admin-ref="sidebar-density"',
    )
    expect(readFileSync(path.join(root, "components/data-table/data-table-shell.tsx"), "utf8")).toContain(
      'data-admin-ref="table-toolbar"',
    )
    expect(readFileSync(path.join(root, "components/layout/app-shell.tsx"), "utf8")).toContain(
      'data-admin-ref="command-actions"',
    )
  })
})
