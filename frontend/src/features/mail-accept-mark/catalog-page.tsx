import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadMailAcceptMarks, type MailAcceptMarkRow } from "@/lib/mail-accept-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { MailAcceptMarkComposer } from "./mark-form"

const helper = createColumnHelper<MailAcceptMarkRow>()
const COLS = [
  helper.accessor("accept_kind", { header: "Tryb" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function MailAcceptMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadMailAcceptMarks,
    queryKey: ["mail-accept-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-mac="split">
      <section className="space-y-3 border-r border-rose-800/20 pr-4">
        <CatalogHeading
          title="Accept z maila"
          subtitle="EXP4.16 · mailto|confirm|reject|other · bez Graph HTTP"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL ślad decyzji z mailto — nie send.</li>
          <li>Bez Graph / IMAP / SMTP.</li>
          <li>Bez drugiego rate_line.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow accept.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              accept_kind: "Tryb",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj accept…"
            tableKey={BUSINESS_LISTS.mailAcceptMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? <TenantSessionNotice /> : <MailAcceptMarkComposer organizationId={organizationId} />}
      </aside>
    </div>
  )
}
