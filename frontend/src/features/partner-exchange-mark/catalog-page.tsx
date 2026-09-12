import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadPartnerExchangeMarks,
  type PartnerExchangeMarkRow,
} from "@/lib/partner-exchange-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PartnerExchangeComposer } from "./mark-form"

const col = createColumnHelper<PartnerExchangeMarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("exchange_kind", { header: "Tryb gieldy" }),
  col.accessor("source_ref", { header: "Zrodlo" }),
]

export function PartnerExchangeBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const board = useQuery({
    enabled: ready,
    queryFn: loadPartnerExchangeMarks,
    queryKey: ["partner-exchange-marks", orgId],
    retry: false,
  })

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-4" data-px="board">
      <CatalogHeading
        title="Gielda partnerska"
        subtitle="EXP2.24 · partner|spot|board · bez live Trans.eu"
      />
      {!ready ? <TenantSessionNotice /> : <PartnerExchangeComposer organizationId={orgId} />}
      {board.error ? <CatalogError error={board.error} /> : null}
      {ready && board.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            exchange_kind: "Tryb gieldy",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={board.data ?? []}
          globalFilterPlaceholder="Filtr gieldy partnerskiej…"
          tableKey={BUSINESS_LISTS.partnerExchangeMark.tableKey}
        />
      ) : null}
    </div>
  )
}
