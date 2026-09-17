import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchRelationDocumentRequirements,
  type RelationDocumentRequirementRow,
} from "@/lib/relation-document-requirements-api"
import { getTenantContext } from "@/lib/tenant"
import { RelationDocumentRequirementSave } from "./mark-form"

const helper = createColumnHelper<RelationDocumentRequirementRow>()

const COLUMNS = [
  helper.accessor("requirement_code", { header: "Kod" }),
  helper.accessor("relation_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function RelationDocumentRequirementDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchRelationDocumentRequirements,
    queryKey: ["relation-document-requirements", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-relation-document-requirement="board">
      <CatalogHeading
        title="Wymog dokumentow relacji"
        subtitle="C8 relation_document_requirement · katalog HITL · nie live 409 na shipment · nie blocks_create"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <RelationDocumentRequirementSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            requirement_code: "Kod",
            relation_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj wymogu dokumentow relacji…"
          tableKey={BUSINESS_LISTS.relationDocumentRequirement.tableKey}
        />
      ) : null}
    </section>
  )
}
