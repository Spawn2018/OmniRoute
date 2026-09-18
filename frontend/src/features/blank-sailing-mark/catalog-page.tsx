import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchBlankSailingMarks,
  type BlankSailingMarkRow,
} from "@/lib/blank-sailing-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { BlankSailingMarkSave } from "./mark-form"

const helper = createColumnHelper<BlankSailingMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("sailing_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function BlankSailingMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchBlankSailingMarks,
    queryKey: ["blank-sailing-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-blank-sailing-mark="board">
      <CatalogHeading
        title="Blank sailing / congestion / Gate OS"
        subtitle="V3 blank_sailing_mark · katalog HITL · nie countdown N3 · nie szkic charge"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <BlankSailingMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            sailing_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika blank sailing…"
          tableKey={BUSINESS_LISTS.blankSailingMark.tableKey}
        />
      ) : null}
    </section>
  )
}
