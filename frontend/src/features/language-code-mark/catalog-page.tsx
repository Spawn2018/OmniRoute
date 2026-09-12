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
  loadLanguageCodeMarks,
  type LanguageCodeMarkRow,
} from "@/lib/language-code-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LanguageCodeMarkComposer } from "./mark-form"

const helper = createColumnHelper<LanguageCodeMarkRow>()
const COLS = [
  helper.accessor("locale_kind", { header: "Locale" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function LanguageCodeMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadLanguageCodeMarks,
    queryKey: ["language-code-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-lcm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Kod jezyka"
          subtitle="EXP1 · pl|en|de|other · bez kolumny shipment"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik kodu jezyka — tylko katalog danych.</li>
          <li>Bez kolumny na shipment i bez preferred_language party.</li>
          <li>Odrębny od i18n UI i od ekstrakcji LLM.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow kodu jezyka.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              locale_kind: "Locale",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika kodu jezyka…"
            tableKey={BUSINESS_LISTS.languageCodeMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <LanguageCodeMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
