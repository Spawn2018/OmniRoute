import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { BlueprintPanel } from "./blueprint-form"

export function BlueprintDesk() {
  const ctx = getTenantContext()
  const signedIn = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-task-template="desk">
      <CatalogHeading
        title="Szablon zadania"
        subtitle="T5 task_template · kod + warunek jako dane · nie worker"
      />
      {signedIn ? (
        <BlueprintPanel organizationId={ctx.organizationId} />
      ) : (
        <TenantSessionNotice />
      )}
    </section>
  )
}
