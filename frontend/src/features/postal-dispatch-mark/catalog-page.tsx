import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchPostalDispatchMarks,
  type PostalDispatchMarkRow,
} from "@/lib/postal-dispatch-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PostalDispatchMarkSave } from "./mark-form"

const helper = createColumnHelper<PostalDispatchMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("dispatch_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function PostalDispatchMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchPostalDispatchMarks,
    queryKey: ["postal-dispatch-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-postal-dispatch-mark="board">
      <CatalogHeading
        title="Ksiazka PP"
        subtitle="F11 postal_dispatch_mark · katalog HITL · nie live PP · nie e-Doreczenia"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PostalDispatchMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            dispatch_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj ksiazki PP…"
          tableKey={BUSINESS_LISTS.postalDispatchMark.tableKey}
        />
      ) : null}
    </section>
  )
}
