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
  loadSlotGuaranteeMarks,
  type SlotGuaranteeMarkRow,
} from "@/lib/slot-guarantee-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SlotGuaranteeMarkComposer } from "./mark-form"

const helper = createColumnHelper<SlotGuaranteeMarkRow>()
const COLS = [
  helper.accessor("stance_kind", { header: "Postawa" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function SlotGuaranteeMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadSlotGuaranteeMarks,
    queryKey: ["slot-guarantee-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-sgm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Stance slotu"
          subtitle="EXP0.3 · capability|non_guarantee|other · bez live T8"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik „slot ≠ gwarancja” — tylko katalog danych.</li>
          <li>Bez live T8 i bez confirmed z formularza.</li>
          <li>Odrębny od terminal_slot_connector (godziny/mode).</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow stance slotu.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              stance_kind: "Postawa",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika stance…"
            tableKey={BUSINESS_LISTS.slotGuaranteeMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <SlotGuaranteeMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
