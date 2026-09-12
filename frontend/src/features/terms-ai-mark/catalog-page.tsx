import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadTermsAiMarks, type TermsAiMarkRow } from "@/lib/terms-ai-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { TermsAiMarkComposer } from "./mark-form"

const helper = createColumnHelper<TermsAiMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod terms" }),
  helper.accessor("terms_kind", { header: "draft / clause / accept" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function TermsAiMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listing = useQuery({
    enabled: ready,
    queryFn: loadTermsAiMarks,
    queryKey: ["terms-ai-marks", orgId],
    retry: false,
  })
  const rows = listing.data ?? []
  const tableOk = ready && listing.error == null

  return (
    <article className="space-y-4 bg-stone-100/50 p-5 dark:bg-stone-950/20" data-tai="board">
      <CatalogHeading title="Terms AI" subtitle="EXP4.15 · draft|clause|accept|other · nie CI blob" />
      <p className="text-sm text-muted-foreground">
        Znacznik terms / klauzuli AI jako dana HITL. Bez blobu CI9 i bez auto-accept.
      </p>
      {!ready ? <TenantSessionNotice /> : <TermsAiMarkComposer organizationId={orgId} />}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {tableOk && rows.length === 0 ? (
        <p className="text-sm text-muted-foreground">Brak znacznikow terms.</p>
      ) : null}
      {tableOk ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod terms",
            terms_kind: "draft / clause / accept",
            source_ref: "Zrodlo",
          }}
          columns={COLS}
          data={rows}
          globalFilterPlaceholder="Filtr terms…"
          tableKey={BUSINESS_LISTS.termsAiMark.tableKey}
        />
      ) : null}
    </article>
  )
}
