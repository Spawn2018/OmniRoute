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
  loadPostingMarks,
  type PostingMarkRow,
} from "@/lib/posting-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PostingMarkComposer } from "./mark-form"

const helper = createColumnHelper<PostingMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod posting" }),
  helper.accessor("posting_kind", { header: "Rodzaj delegowania" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function PostingMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listing = useQuery({
    enabled: ready,
    queryFn: loadPostingMarks,
    queryKey: ["posting-marks", orgId],
    retry: false,
  })
  const rows = listing.data ?? []
  const tableOk = ready && listing.error == null

  return (
    <section
      className="space-y-4 bg-sky-50/40 p-4 ring-1 ring-sky-800/15 dark:bg-sky-950/20"
      data-po="board"
    >
      <CatalogHeading
        title="Posting"
        subtitle="EXP4.9 · posting|delegation|host|other · bez live API"
      />
      <p className="text-sm text-muted-foreground">
        Znacznik posting / delegowania jako dana. Nie wylicza prawa per kraj i nie czyta
        tacho DDD.
      </p>
      {!ready ? <TenantSessionNotice /> : <PostingMarkComposer organizationId={orgId} />}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {tableOk && rows.length === 0 ? (
        <p className="text-sm text-muted-foreground">Brak wpisow posting — dodaj HITL.</p>
      ) : null}
      {tableOk ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod posting",
            posting_kind: "Rodzaj delegowania",
            source_ref: "Zrodlo",
          }}
          columns={COLS}
          data={rows}
          globalFilterPlaceholder="Filtr posting…"
          tableKey={BUSINESS_LISTS.postingMark.tableKey}
        />
      ) : null}
    </section>
  )
}
