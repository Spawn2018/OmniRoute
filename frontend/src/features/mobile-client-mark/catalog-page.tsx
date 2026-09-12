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
  loadMobileClientMarks,
  type MobileClientMarkRow,
} from "@/lib/mobile-client-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { MobileClientMarkComposer } from "./mark-form"

const helper = createColumnHelper<MobileClientMarkRow>()
const COLS = [
  helper.accessor("client_kind", { header: "Klient" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function MobileClientMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadMobileClientMarks,
    queryKey: ["mobile-client-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-mcm="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="Klient mobilny"
          subtitle="Mob · ios|android|ota|other · bez Expo/EAS"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik klienta mobilnego — tylko katalog danych.</li>
          <li>Bez Expo app i EAS OTA live.</li>
          <li>Bez store submit i kwoty.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow klienta mobilnego.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              client_kind: "Klient",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj klienta mobilnego…"
            tableKey={BUSINESS_LISTS.mobileClientMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <MobileClientMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
