import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadAbandonedRtoMarks,
  type AbandonedRtoMarkRow,
} from "@/lib/abandoned-rto-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { AbandonedRtoComposer } from "./mark-form"

const helper = createColumnHelper<AbandonedRtoMarkRow>()
const ARO_COLS = [
  helper.accessor("mark_code", { header: "Kod losu" }),
  helper.accessor("fate_kind", { header: "Abandoned / RTO" }),
  helper.accessor("source_ref", { header: "Zrodlo HITL" }),
]

export function AbandonedRtoBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const signedIn = Boolean(organizationId && tenant.userId)
  const catalog = useQuery({
    enabled: signedIn,
    queryFn: loadAbandonedRtoMarks,
    queryKey: ["abandoned-rto-marks", organizationId],
    retry: false,
  })
  const rows = catalog.data ?? []

  return (
    <section className="space-y-5 bg-amber-50/40 p-3 dark:bg-amber-950/10" data-aro="panel">
      <CatalogHeading
        title="Abandoned i RTO"
        subtitle="EXP3.10 · fate HITL abandoned|rto|return|other · bez live"
      />
      <p className="max-w-2xl text-xs text-muted-foreground">
        Znacznik losu przesylki — nie auto RTO i nie druga tabela shipment.
      </p>
      {signedIn ? (
        <AbandonedRtoComposer organizationId={organizationId} />
      ) : (
        <TenantSessionNotice />
      )}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {signedIn && catalog.error == null && rows.length === 0 ? (
        <p className="text-sm italic text-muted-foreground">Pusto — dodaj pierwszy los HITL.</p>
      ) : null}
      {signedIn && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod losu",
            fate_kind: "Abandoned / RTO",
            source_ref: "Zrodlo HITL",
          }}
          columns={ARO_COLS}
          data={rows}
          globalFilterPlaceholder="Szukaj abandoned/RTO…"
          tableKey={BUSINESS_LISTS.abandonedRtoMark.tableKey}
        />
      ) : null}
    </section>
  )
}
