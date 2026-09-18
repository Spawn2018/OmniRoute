import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchDocumentKindMatchMarks,
  type DocumentKindMatchMarkRow,
} from "@/lib/document-kind-match-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { DocumentKindMatchMarkSave } from "./mark-form"

const helper = createColumnHelper<DocumentKindMatchMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("match_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function DocumentKindMatchMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchDocumentKindMatchMarks,
    queryKey: ["document-kind-match-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-document-kind-match-mark="board">
      <CatalogHeading
        title="Dopasowanie rodzaju dokumentu"
        subtitle="C8 document_kind_match_mark · katalog HITL · nie live matching · nie party_document SQL"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <DocumentKindMatchMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            match_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj dopasowania rodzaju dokumentu…"
          tableKey={BUSINESS_LISTS.documentKindMatchMark.tableKey}
        />
      ) : null}
    </section>
  )
}
