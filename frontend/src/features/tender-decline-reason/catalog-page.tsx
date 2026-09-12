import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadTenderDeclineReasons,
  type TenderDeclineReasonRow,
} from "@/lib/tender-decline-reasons-api"
import { getTenantContext } from "@/lib/tenant"
import { TenderDeclineReasonComposer } from "./mark-form"

const helper = createColumnHelper<TenderDeclineReasonRow>()
const TDR_COLS = [
  helper.accessor("mark_code", { header: "Kod powodu" }),
  helper.accessor("decline_kind", { header: "Decline / no-bid" }),
  helper.accessor("source_ref", { header: "Zrodlo HITL" }),
]

export function TenderDeclineReasonBoard() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const ready = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: ready,
    queryFn: loadTenderDeclineReasons,
    queryKey: ["tender-decline-reasons", organizationId],
    retry: false,
  })
  const rows = catalog.data ?? []

  return (
    <section
      className="mx-auto flex max-w-4xl flex-col gap-5 border-l-8 border-rose-700/50 pl-4"
      data-tdr="workspace"
    >
      <header className="space-y-2">
        <CatalogHeading
          title="Powody tender decline"
          subtitle="EXP3.12 · HITL decline|no_bid|withdraw|other · bez auto-award"
        />
        <ul className="list-inside list-disc text-[11px] text-muted-foreground">
          <li>Nie win/loss i nie extract RFP.</li>
          <li>OTIF split pominięty — katalog `otif_mark` juz istnieje.</li>
        </ul>
      </header>
      {ready ? (
        <TenderDeclineReasonComposer organizationId={organizationId} />
      ) : (
        <TenantSessionNotice />
      )}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {ready && catalog.error == null && rows.length === 0 ? (
        <p className="rounded border border-dashed p-2 text-sm text-muted-foreground">
          Brak wpisow — dodaj powod HITL.
        </p>
      ) : null}
      {ready && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod powodu",
            decline_kind: "Decline / no-bid",
            source_ref: "Zrodlo HITL",
          }}
          columns={TDR_COLS}
          data={rows}
          globalFilterPlaceholder="Szukaj powodow decline…"
          tableKey={BUSINESS_LISTS.tenderDeclineReason.tableKey}
        />
      ) : null}
    </section>
  )
}
