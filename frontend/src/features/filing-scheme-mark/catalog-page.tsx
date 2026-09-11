import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchFilingSchemeMarks,
  type FilingSchemeMarkRow,
} from "@/lib/filing-scheme-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FilingSchemeMarkSave } from "./mark-form"

const helper = createColumnHelper<FilingSchemeMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("scheme_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function FilingSchemeMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchFilingSchemeMarks,
    queryKey: ["filing-scheme-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-filing-scheme-mark="board">
      <CatalogHeading
        title="Schemat składania"
        subtitle="G12 filing_scheme_mark · katalog HITL · nie SENT-UE · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <FilingSchemeMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            scheme_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj schematu składania…"
          tableKey={BUSINESS_LISTS.filingSchemeMark.tableKey}
        />
      ) : null}
    </section>
  )
}
