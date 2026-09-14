import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchStyleFidelityMarks,
  type StyleFidelityMarkRow,
} from "@/lib/style-fidelity-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { StyleFidelityMarkSave } from "./mark-form"

const helper = createColumnHelper<StyleFidelityMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("fidelity_kind", { header: "Stancja" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function StyleFidelityMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchStyleFidelityMarks,
    queryKey: ["style-fidelity-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-style-fidelity-mark="board">
      <CatalogHeading
        title="STYLE FIDELITY"
        subtitle="AI8.1 style_fidelity_mark · HITL pass/hold/reject/exempt · nie score · nie scoring osoby"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <StyleFidelityMarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            fidelity_kind: "Stancja",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj stancje fidelity…"
          tableKey={BUSINESS_LISTS.styleFidelityMark.tableKey}
        />
      ) : null}
    </section>
  )
}
