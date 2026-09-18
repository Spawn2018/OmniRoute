import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchFilingFkMarks,
  type FilingFkMarkRow,
} from "@/lib/filing-fk-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FilingFkMarkSave } from "./mark-form"

const helper = createColumnHelper<FilingFkMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("fk_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function FilingFkMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchFilingFkMarks,
    queryKey: ["filing-fk-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-filing-fk-mark="board">
      <CatalogHeading
        title="Cel FK zgłoszenia"
        subtitle="C1 filing_fk_mark · katalog HITL · nie live FK UUID · nie PUESC"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <FilingFkMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            fk_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj celu FK…"
          tableKey={BUSINESS_LISTS.filingFkMark.tableKey}
        />
      ) : null}
    </section>
  )
}
