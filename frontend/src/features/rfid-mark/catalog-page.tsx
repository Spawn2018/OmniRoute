import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchRfidMarks, type RfidMarkRow } from "@/lib/rfid-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { RfidMarkSave } from "./mark-form"

const helper = createColumnHelper<RfidMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("rfid_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function RfidMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchRfidMarks,
    queryKey: ["rfid-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-rfid-mark="board">
      <CatalogHeading
        title="RFID magazyn"
        subtitle="BR1.1 rfid_mark · katalog HITL · nie live poll · nie EPC"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <RfidMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            rfid_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znaczników RFID…"
          tableKey={BUSINESS_LISTS.rfidMark.tableKey}
        />
      ) : null}
    </section>
  )
}
