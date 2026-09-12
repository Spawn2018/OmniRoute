import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadMqcMarks, type MqcMarkRow } from "@/lib/mqc-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { MqcComposer } from "./mark-form"

const cols = createColumnHelper<MqcMarkRow>()
const COLS = [
  cols.accessor("mark_code", { header: "Kod MQC" }),
  cols.accessor("mqc_kind", { header: "Rodzaj" }),
  cols.accessor("source_ref", { header: "Ref" }),
]

export function MqcBoard() {
  const t = getTenantContext()
  const org = t.organizationId
  const ok = Boolean(org && t.userId)
  const q = useQuery({
    enabled: ok,
    queryFn: loadMqcMarks,
    queryKey: ["mqc-marks", org],
    retry: false,
  })
  return (
    <div className="grid gap-3" data-mqc="root">
      <CatalogHeading title="MQC" subtitle="EXP3.5 · mqc|actual|gap · bez MQC SQL" />
      {ok ? <MqcComposer organizationId={org} /> : <TenantSessionNotice />}
      {q.error ? <CatalogError error={q.error} /> : null}
      {ok && !q.error ? (
        <DataTableShell
          columnLabels={{ mark_code: "Kod MQC", mqc_kind: "Rodzaj", source_ref: "Ref" }}
          columns={COLS}
          data={q.data ?? []}
          globalFilterPlaceholder="Szukaj MQC…"
          tableKey={BUSINESS_LISTS.mqcMark.tableKey}
        />
      ) : null}
    </div>
  )
}
