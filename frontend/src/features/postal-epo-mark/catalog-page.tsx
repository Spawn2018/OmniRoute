import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchPostalEpoMarks, type PostalEpoMarkRow } from "@/lib/postal-epo-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PostalEpoMarkSave } from "./mark-form"

const helper = createColumnHelper<PostalEpoMarkRow>()
const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("epo_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function PostalEpoMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchPostalEpoMarks,
    queryKey: ["postal-epo-marks", orgId],
    retry: false,
  })
  return (
    <section className="flex flex-col gap-5" data-postal-epo-mark="board">
      <CatalogHeading
        title="Znacznik EPO/PP"
        subtitle="C1 postal_epo_mark Â· katalog HITL Â· nie live PP/scheme Â· nie e-DorÄ™czenia"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <PostalEpoMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{ mark_code: "Kod", epo_kind: "Rodzaj", source_ref: "Pochodzenie" }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika EPOâ€¦"
          tableKey={BUSINESS_LISTS.postalEpoMark.tableKey}
        />
      ) : null}
    </section>
  )
}
