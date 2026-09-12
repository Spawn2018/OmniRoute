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
  loadHaulierRoleMarks,
  type HaulierRoleMarkRow,
} from "@/lib/haulier-role-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { HaulierRoleMarkComposer } from "./mark-form"

const helper = createColumnHelper<HaulierRoleMarkRow>()
const COLS = [
  helper.accessor("role_kind", { header: "Rola" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function HaulierRoleMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadHaulierRoleMarks,
    queryKey: ["haulier-role-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-hrm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Rola przewoznika"
          subtitle="EXP1 · booked|actual|other · bez FK party"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik roli przewoznika — tylko katalog danych.</li>
          <li>Bez FK party na shipment i bez cargo_value.</li>
          <li>Odrębny od booked_carrier vs actual_haulier na zleceniu.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow roli przewoznika.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              role_kind: "Rola",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika roli przewoznika…"
            tableKey={BUSINESS_LISTS.haulierRoleMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <HaulierRoleMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
