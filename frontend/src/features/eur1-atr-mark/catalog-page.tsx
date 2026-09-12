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
  loadEur1AtrMarks,
  type Eur1AtrMarkRow,
} from "@/lib/eur1-atr-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { Eur1AtrComposer } from "./mark-form"

const tableHelper = createColumnHelper<Eur1AtrMarkRow>()
const EUR1_COLUMNS = [
  tableHelper.accessor("mark_code", { header: "Numer swiadectwa" }),
  tableHelper.accessor("cert_kind", { header: "Typ certyfikatu" }),
  tableHelper.accessor("source_ref", { header: "Pochodzenie HITL" }),
]

export function Eur1AtrBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: loadEur1AtrMarks,
    queryKey: ["eur1-atr-marks", organizationId],
    retry: false,
  })

  return (
    <main className="mx-auto flex max-w-5xl flex-col gap-5 py-2" data-eur1="workspace">
      <CatalogHeading
        title="Swiadectwa EUR.1 i ATR"
        subtitle="EXP3.7 · katalog HITL · eur1|atr|origin|other · bez live"
      />
      {sessionReady ? (
        <Eur1AtrComposer organizationId={organizationId} />
      ) : (
        <TenantSessionNotice />
      )}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Numer swiadectwa",
            cert_kind: "Typ certyfikatu",
            source_ref: "Pochodzenie HITL",
          }}
          columns={EUR1_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtruj swiadectwa EUR.1/ATR…"
          tableKey={BUSINESS_LISTS.eur1AtrMark.tableKey}
        />
      ) : null}
    </main>
  )
}
