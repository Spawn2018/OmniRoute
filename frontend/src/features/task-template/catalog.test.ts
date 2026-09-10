import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { blueprintWrite } from "@/lib/task-templates-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("blueprintWrite", () => {
  it("trims code and condition without money math", () => {
    expect(
      blueprintWrite({
        codeToken: " Gate-In ",
        whenNote: " CY cutoff ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      template_code: "Gate-In",
      applies_when: "CY cutoff",
      source_ref: "tenant:manual",
    })
  })
})

describe("task_template surface for 263.0", () => {
  it("records a HITL blueprint on /task-templates without Money or matching", () => {
    const page = src("features/task-template/catalog-page.tsx")
    const form = src("features/task-template/blueprint-form.tsx")
    expect(src("routes/task-templates.tsx")).toContain("/task-templates")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/task-templates"')
    expect(src("lib/business-lists.ts")).toContain("taskTemplate")
    expect(page).toContain('data-task-template="desk"')
    expect(page).toContain("BlueprintPanel")
    expect(form).toContain("persistTaskTemplate")
    expect(form).not.toContain("<Money")
    expect(form).toContain("Zapisz szablon zadania")
    expect(form).not.toContain("parseFloat")
    expect(form).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"263.0": "/task-templates"')
  })
})
