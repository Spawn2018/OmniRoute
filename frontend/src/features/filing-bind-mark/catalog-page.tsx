import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchFilingBindMarks, type FilingBindMarkRow } from "@/lib/filing-bind-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FilingBindMarkSave } from "./mark-form"

const helper = createColumnHelper<FilingBindMarkRow>()
const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("bind_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function FilingBindMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchFilingBindMarks,
    queryKey: ["filing-bind-marks", orgId],
    retry: false,
  })
  return (
    <section className="flex flex-col gap-5" data-filing-bind-mark="board">
      <CatalogHeading
        title="Wiązanie zgłoszenia SENT/BDO"
        subtitle="C1 filing_bind_mark · katalog HITL · nie FK shipment/scheme · nie PUESC"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <FilingBindMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{ mark_code: "Kod", bind_kind: "Rodzaj", source_ref: "Pochodzenie" }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj wiązania zgłoszenia…"
          tableKey={BUSINESS_LISTS.filingBindMark.tableKey}
        />
      ) : null}
    </section>
  )
}
