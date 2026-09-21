import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { TaskPanel } from "./task-form"

export function TaskDesk() {
  const ctx = getTenantContext()
  const signedIn = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-task="desk">
      <CatalogHeading
        title="Zadanie"
        subtitle="T5 task · kod + szablon + status HITL · nie matching"
      />
      {signedIn ? (
        <TaskPanel organizationId={ctx.organizationId} />
      ) : (
        <TenantSessionNotice />
      )}
    </section>
  )
}
