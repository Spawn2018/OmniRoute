import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadOffboardingMarks,
  type OffboardingMarkRow,
} from "@/lib/offboarding-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { OffboardingComposer } from "./mark-form"

const col = createColumnHelper<OffboardingMarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("offboard_kind", { header: "Tryb offboard" }),
  col.accessor("source_ref", { header: "Zrodlo" }),
]

export function OffboardingBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const list = useQuery({
    enabled: ready,
    queryFn: loadOffboardingMarks,
    queryKey: ["offboarding-marks", orgId],
    retry: false,
  })

  return (
    <div className="flex flex-col gap-4" data-ob="board">
      <CatalogHeading
        title="Offboarding"
        subtitle="EXP2.28 · offboard|export|revoke · bez wipe ciphertext"
      />
      {!ready ? <TenantSessionNotice /> : <OffboardingComposer organizationId={orgId} />}
      {list.error ? <CatalogError error={list.error} /> : null}
      {ready && list.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            offboard_kind: "Tryb offboard",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={list.data ?? []}
          globalFilterPlaceholder="Szukaj offboarding…"
          tableKey={BUSINESS_LISTS.offboardingMark.tableKey}
        />
      ) : null}
    </div>
  )
}
