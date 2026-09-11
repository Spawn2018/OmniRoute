import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchCalibrationMarks,
  type CalibrationMarkRow,
} from "@/lib/calibration-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CalibrationMarkSave } from "./mark-form"

const helper = createColumnHelper<CalibrationMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("sample_ready", { header: "Gotowość" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CalibrationMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCalibrationMarks,
    queryKey: ["calibration-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-calibration-mark="board">
      <CatalogHeading
        title="Znacznik kalibracji"
        subtitle="CI7 calibration_mark · katalog HITL · nie MAE SQL · nie float"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CalibrationMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            sample_ready: "Gotowość",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika kalibracji…"
          tableKey={BUSINESS_LISTS.calibrationMark.tableKey}
        />
      ) : null}
    </section>
  )
}
