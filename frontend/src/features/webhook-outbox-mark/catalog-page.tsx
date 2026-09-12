import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadWebhookOutboxMarks,
  type WebhookOutboxMarkRow,
} from "@/lib/webhook-outbox-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { WebhookOutboxComposer } from "./mark-form"

const col = createColumnHelper<WebhookOutboxMarkRow>()
const COLUMNS = [
  col.accessor("mark_code", { header: "Kod" }),
  col.accessor("outbox_kind", { header: "Tryb outbox" }),
  col.accessor("source_ref", { header: "Źródło" }),
]

export function WebhookOutboxBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const rows = useQuery({
    enabled: ready,
    queryFn: loadWebhookOutboxMarks,
    queryKey: ["webhook-outbox-marks", orgId],
    retry: false,
  })

  return (
    <main className="flex flex-col gap-4 p-1" data-wh="outbox-board">
      <CatalogHeading
        title="Webhook outbox"
        subtitle="EXP2.23 · webhook|retry|dead · bez live dispatch"
      />
      {!ready ? <TenantSessionNotice /> : <WebhookOutboxComposer organizationId={orgId} />}
      {rows.error ? <CatalogError error={rows.error} /> : null}
      {ready && rows.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            outbox_kind: "Tryb outbox",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={rows.data ?? []}
          globalFilterPlaceholder="Szukaj znacznika outbox…"
          tableKey={BUSINESS_LISTS.webhookOutboxMark.tableKey}
        />
      ) : null}
    </main>
  )
}
