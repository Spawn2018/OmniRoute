import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchRemediationOptions,
  type RemediationOptionRow,
} from "@/lib/remediation-options-api"
import { getTenantContext } from "@/lib/tenant"
import { RemediationOptionSave } from "./option-form"

const helper = createColumnHelper<RemediationOptionRow>()

const COLUMNS = [
  helper.accessor("option_code", { header: "Kod" }),
  helper.accessor("option_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function RemediationOptionDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchRemediationOptions,
    queryKey: ["remediation-options", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-remediation-option="board">
      <CatalogHeading
        title="Opcja naprawy"
        subtitle="CI6 remediation_option · katalog HITL · nie kwota · nie S11"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <RemediationOptionSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            option_code: "Kod",
            option_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj opcji naprawy…"
          tableKey={BUSINESS_LISTS.remediationOption.tableKey}
        />
      ) : null}
    </section>
  )
}
