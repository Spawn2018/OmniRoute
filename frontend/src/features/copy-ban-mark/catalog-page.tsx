import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadCopyBanMarks, type CopyBanMarkRow } from "@/lib/copy-ban-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CopyBanMarkComposer } from "./mark-form"

const helper = createColumnHelper<CopyBanMarkRow>()
const COLS = [
  helper.accessor("ban_kind", { header: "Zakaz" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function CopyBanMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadCopyBanMarks,
    queryKey: ["copy-ban-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-cbm="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="Zakaz copy claimów"
          subtitle="EXP4.19 · eight_min|fifteen_k|five_hundred_k|other · bez copy marketingu"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik zakazu copy claimów — tylko katalog danych.</li>
          <li>Bez copy claimów 8min/15k/500k do UI.</li>
          <li>Bez silnika banów i Bayer live scrape.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow zakazu copy.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              ban_kind: "Zakaz",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj zakazu copy…"
            tableKey={BUSINESS_LISTS.copyBanMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <CopyBanMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
