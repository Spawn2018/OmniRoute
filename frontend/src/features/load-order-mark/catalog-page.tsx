import { useQuery } from "@tanstack/react-query"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { loadLoadOrderMarks } from "@/lib/load-order-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LoadOrderMarkSave } from "./mark-form"

export function LoadOrderMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const sessionReady = Boolean(orgId && ctx.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: loadLoadOrderMarks,
    queryKey: ["load-order-marks", orgId],
    retry: false,
  })
  const rows = catalog.data ?? []

  return (
    <section className="flex flex-col gap-5" data-load-order-mark="board">
      <CatalogHeading
        title="Kolejność załadunku"
        subtitle="BR3.1 load_order_mark · katalog HITL · nie solver · nie wymiary Decimal"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <LoadOrderMarkSave organizationId={orgId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <table className="w-full max-w-3xl text-left text-sm" data-load-order-mark="rows">
          <caption className="sr-only">Katalog kolejności załadunku</caption>
          <thead>
            <tr>
              <th>Kod</th>
              <th>Rodzaj</th>
              <th>Pochodzenie</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id}>
                <td className="font-mono">{row.mark_code}</td>
                <td>{row.order_kind}</td>
                <td className="font-mono">{row.source_ref}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </section>
  )
}
