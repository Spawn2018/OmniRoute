import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchBondedMarks, type BondedMarkRow } from "@/lib/bonded-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { BondedMarkSave } from "./mark-form"

const helper = createColumnHelper<BondedMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("bond_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function BondedMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchBondedMarks,
    queryKey: ["bonded-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-bonded-mark="board">
      <CatalogHeading
        title="Znacznik bonded"
        subtitle="G11 bonded_mark · katalog HITL · nie WMS · nie kwota"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <BondedMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            bond_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika bonded…"
          tableKey={BUSINESS_LISTS.bondedMark.tableKey}
        />
      ) : null}
    </section>
  )
}
