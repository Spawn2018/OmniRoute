import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadRagSopMarks, type RagSopMarkRow } from "@/lib/rag-sop-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { RagSopMarkComposer } from "./mark-form"

const helper = createColumnHelper<RagSopMarkRow>()
const COLS = [
  helper.accessor("scope_kind", { header: "Zakres" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function RagSopMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadRagSopMarks,
    queryKey: ["rag-sop-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-rsm="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="Zakres RAG"
          subtitle="EXP4.18 · sop|adr|mail|other · bez pgvector"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik zakresu RAG — tylko SOP/ADR/mail.</li>
          <li>Bez pgvector i embedding live.</li>
          <li>Bez RAG na wycenie i schemacie DB.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow zakresu RAG.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              scope_kind: "Zakres",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj zakresu RAG…"
            tableKey={BUSINESS_LISTS.ragSopMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <RagSopMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
