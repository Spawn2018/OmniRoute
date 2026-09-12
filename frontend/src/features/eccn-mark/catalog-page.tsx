import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadEccnMarks, type EccnMarkRow } from "@/lib/eccn-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { EccnComposer } from "./mark-form"

const helper = createColumnHelper<EccnMarkRow>()
const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod kontroli" }),
  helper.accessor("control_kind", { header: "Tryb" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function EccnBoard() {
  const session = getTenantContext()
  const orgId = session.organizationId
  const ready = Boolean(orgId && session.userId)
  const list = useQuery({
    enabled: ready,
    queryFn: loadEccnMarks,
    queryKey: ["eccn-marks", orgId],
    retry: false,
  })
  return (
    <article className="flex flex-col gap-4" data-eccn="page">
      <CatalogHeading title="ECCN" subtitle="EXP3.6 · eccn|ear|license · bez live" />
      {ready ? <EccnComposer organizationId={orgId} /> : <TenantSessionNotice />}
      {list.error ? <CatalogError error={list.error} /> : null}
      {ready && list.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod kontroli",
            control_kind: "Tryb",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={list.data ?? []}
          globalFilterPlaceholder="Filtruj ECCN…"
          tableKey={BUSINESS_LISTS.eccnMark.tableKey}
        />
      ) : null}
    </article>
  )
}
