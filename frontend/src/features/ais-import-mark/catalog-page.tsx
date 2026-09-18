import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchAisImportMarks,
  type AisImportMarkRow,
} from "@/lib/ais-import-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { AisImportMarkSave } from "./mark-form"

const helper = createColumnHelper<AisImportMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("import_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function AisImportMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchAisImportMarks,
    queryKey: ["ais-import-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-ais-import-mark="board">
      <CatalogHeading
        title="AIS / AES / Intrastat"
        subtitle="C2 ais_import_mark · katalog HITL · nie PUESC live · nie XML"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <AisImportMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            import_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika AIS…"
          tableKey={BUSINESS_LISTS.aisImportMark.tableKey}
        />
      ) : null}
    </section>
  )
}
