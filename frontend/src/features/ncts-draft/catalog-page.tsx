import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchNctsDrafts, type NctsDraftRow } from "@/lib/ncts-drafts-api"
import { getTenantContext } from "@/lib/tenant"
import { NctsDraftSave } from "./mark-form"

const helper = createColumnHelper<NctsDraftRow>()

const COLUMNS = [
  helper.accessor("draft_code", { header: "Kod" }),
  helper.accessor("transit_kind", { header: "Tranzyt" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function NctsDraftDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchNctsDrafts,
    queryKey: ["ncts-drafts", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-ncts-draft="board">
      <CatalogHeading
        title="Szkic NCTS"
        subtitle="G4 ncts_draft · katalog HITL · nie PUESC · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <NctsDraftSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            draft_code: "Kod",
            transit_kind: "Tranzyt",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj szkicu NCTS…"
          tableKey={BUSINESS_LISTS.nctsDraft.tableKey}
        />
      ) : null}
    </section>
  )
}
