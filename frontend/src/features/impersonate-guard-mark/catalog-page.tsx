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
  loadImpersonateGuardMarks,
  type ImpersonateGuardMarkRow,
} from "@/lib/impersonate-guard-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ImpersonateGuardMarkComposer } from "./mark-form"

const helper = createColumnHelper<ImpersonateGuardMarkRow>()
const COLS = [
  helper.accessor("guard_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function ImpersonateGuardMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadImpersonateGuardMarks,
    queryKey: ["impersonate-guard-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-igm="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="Impersonate guard"
          subtitle="EXP0.12 · impersonate|unwrap_denied|other · bez unwrap"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik reguły Admin-P — tylko katalog danych.</li>
          <li>Impersonate ≠ decrypt/unwrap umów.</li>
          <li>Bez crypto, KMS, Fernet i Auth0 live.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow impersonate guard.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              guard_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj impersonate guard…"
            tableKey={BUSINESS_LISTS.impersonateGuardMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <ImpersonateGuardMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
