import { CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { getTenantContext } from "@/lib/tenant"
import { EdgeBoard } from "./edge-board"

export function EdgeDesk() {
  const tenant = getTenantContext()
  const signedIn = tenant.organizationId !== null && tenant.userId !== null
  return (
    <section className="space-y-5" data-memory-edge="desk">
      <CatalogHeading
        title="Krawędź pamięci"
        subtitle="W3 memory_edge · rodzaj krawędzi · nie wyszukiwanie stawek"
      />
      {signedIn ? <EdgeBoard organizationId={tenant.organizationId} /> : <TenantSessionNotice />}
    </section>
  )
}
