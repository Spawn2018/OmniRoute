import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchAeoDossierMarks, type AeoDossierMarkRow } from "@/lib/aeo-dossier-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { AeoDossierMarkSave } from "./mark-form"

const helper = createColumnHelper<AeoDossierMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("dossier_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function AeoDossierMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchAeoDossierMarks,
    queryKey: ["aeo-dossier-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-aeo-dossier-mark="board">
      <CatalogHeading
        title="Dossier AEO"
        subtitle="G14 aeo_dossier_mark · katalog HITL · nie party_document · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <AeoDossierMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            dossier_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj dossier AEO…"
          tableKey={BUSINESS_LISTS.aeoDossierMark.tableKey}
        />
      ) : null}
    </section>
  )
}
