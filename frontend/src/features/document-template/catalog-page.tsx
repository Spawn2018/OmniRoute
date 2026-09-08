import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { SheetKindPanel } from "./sheet-panel"

export function DocumentTemplateBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-document-template="board">
      <CatalogHeading
        title="Szablony wydruku"
        subtitle="D9 document_template · layout jako dane · nie PDF · nie etykieta sieci"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SheetKindPanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
