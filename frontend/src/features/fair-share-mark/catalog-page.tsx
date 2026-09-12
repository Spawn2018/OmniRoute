import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadFairShareMarks,
  type FairShareMarkRow,
} from "@/lib/fair-share-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FairShareComposer } from "./mark-form"

const helper = createColumnHelper<FairShareMarkRow>()
const TABLE_COLS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("share_kind", { header: "Udzial" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function FairShareBoard() {
  const ctx = getTenantContext()
  const organizationId = ctx.organizationId
  const sessionOk = Boolean(organizationId && ctx.userId)
  const catalog = useQuery({
    enabled: sessionOk,
    queryFn: loadFairShareMarks,
    queryKey: ["fair-share-marks", organizationId],
    retry: false,
  })

  return (
    <main className="space-y-5 p-1" data-fs="panel">
      <CatalogHeading
        title="Fair share"
        subtitle="EXP3.4 · fair|split|pool · bez allocation SQL"
      />
      {sessionOk ? (
        <FairShareComposer organizationId={organizationId} />
      ) : (
        <TenantSessionNotice />
      )}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionOk && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            share_kind: "Udzial",
            source_ref: "Pochodzenie",
          }}
          columns={TABLE_COLS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtruj fair share…"
          tableKey={BUSINESS_LISTS.fairShareMark.tableKey}
        />
      ) : null}
    </main>
  )
}
