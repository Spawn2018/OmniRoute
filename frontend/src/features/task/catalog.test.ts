import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { taskWrite } from "@/lib/tasks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("taskWrite", () => {
  it("trims task fields without money math", () => {
    expect(
      taskWrite({
        codeToken: " gate_check_01 ",
        templateToken: " gate_in ",
        statusToken: " open ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      task_code: "gate_check_01",
      template_code: "gate_in",
      status_kind: "open",
      source_ref: "tenant:manual",
    })
  })
})

describe("task surface for 616.0", () => {
  it("maps plaster to /tasks without Money or matching", () => {
    expect(SHIPPED_CHARGE_ROUTES["616.0"]).toBe("/tasks")
    const page = src("features/task/catalog-page.tsx")
    const form = src("features/task/task-form.tsx")
    expect(src("routes/tasks.tsx")).toContain("/tasks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tasks"')
    expect(src("lib/business-lists.ts")).toContain("task:")
    expect(page).toContain('data-task="desk"')
    expect(page).toContain("TaskPanel")
    expect(form).toContain("persistTask")
    expect(form).not.toContain("<Money")
    expect(form).toContain("Zapisz zadanie")
    expect(form).not.toContain("parseFloat")
  })
})
