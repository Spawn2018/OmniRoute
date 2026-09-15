import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchArticle50Marks,
  type Article50MarkRow,
} from "@/lib/article50-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { Article50MarkSave } from "./mark-form"

const helper = createColumnHelper<Article50MarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Oznaczenie" }),
  helper.accessor("label_kind", { header: "Etykieta" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function Article50MarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchArticle50Marks,
    queryKey: ["article50-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-article50-mark="board">
      <CatalogHeading
        title="Art. 50"
        subtitle="AI9.0 article50_mark · HITL generated/exempt/human · nie U-art50 UI · nie live LLM"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <Article50MarkSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Oznaczenie",
            label_kind: "Etykieta",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj etykiety art. 50…"
          tableKey={BUSINESS_LISTS.article50Mark.tableKey}
        />
      ) : null}
    </section>
  )
}
