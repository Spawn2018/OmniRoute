import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listSanctionsMarks, type SanctionsMarkRow } from "@/lib/sanctions-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SanctionsMarkEditor } from "./mark-form"

const helper = createColumnHelper<SanctionsMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("list_kind", { header: "Lista" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function SanctionsMarkDesk() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const rows = useQuery({
    enabled: ready,
    queryFn: listSanctionsMarks,
    queryKey: ["sanctions-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-sanctions-mark="desk">
      <CatalogHeading
        title="Sanctions"
        subtitle="EXP2.5 · HITL sanctions_mark · list_kind OFAC/EU/UN · bez live scrape"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <SanctionsMarkEditor organizationId={orgId} /> : null}
      {rows.error ? <CatalogError error={rows.error} /> : null}
      {ready && !rows.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            list_kind: "Lista",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={rows.data ?? []}
          globalFilterPlaceholder="Filtruj sanctions…"
          tableKey={BUSINESS_LISTS.sanctionsMark.tableKey}
        />
      ) : null}
    </section>
  )
}
