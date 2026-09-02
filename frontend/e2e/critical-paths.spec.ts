import AxeBuilder from "@axe-core/playwright"
import { expect, test, type Page } from "@playwright/test"

async function expectNoSeriousAxe(page: Page): Promise<void> {
  const scan = await new AxeBuilder({ page }).analyze()
  const blocking = scan.violations.filter(
    (violation) => violation.impact === "serious" || violation.impact === "critical",
  )
  expect(blocking, blocking.map((violation) => violation.id).join(",")).toEqual([])
}

test("session then rate lines", async ({ page }) => {
  await page.goto("/session")
  await expect(page.getByRole("heading", { name: "Sesja" })).toBeVisible()
  await expectNoSeriousAxe(page)
  await page.goto("/rate-lines")
  await expect(page.getByRole("heading", { name: "Stawki kupna" })).toBeVisible()
  await expectNoSeriousAxe(page)
})

test("HITL queue without accept", async ({ page }) => {
  await page.goto("/extractions")
  await expect(page.getByRole("heading", { name: "Kolejka ekstrakcji (HITL)" })).toBeVisible()
  await expect(page.getByRole("button", { name: "Akceptuj" })).toHaveCount(0)
  await expectNoSeriousAxe(page)
})

test("quotation catalog", async ({ page }) => {
  await page.goto("/quotations")
  await expect(page.getByRole("heading", { name: "Wyceny" })).toBeVisible()
  await expectNoSeriousAxe(page)
})
