import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchNacMarks, type NacMarkRow } from "@/lib/nac-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { NacMarkSave } from "./mark-form"

const helper = createColumnHelper<NacMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("nac_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function NacMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchNacMarks,
    queryKey: ["nac-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-nac-mark="board">
      <CatalogHeading
        title="NAC i agent nominowany"
        subtitle="BR4.3 nac_mark · katalog HITL · nie live NAC HTTP · nie FK stakeholder"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <NacMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            nac_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj stance NAC…"
          tableKey={BUSINESS_LISTS.nacMark.tableKey}
        />
      ) : null}
    </section>
  )
}
