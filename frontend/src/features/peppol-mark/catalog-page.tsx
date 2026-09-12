import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchPeppolMarks, type PeppolMarkRow } from "@/lib/peppol-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { PeppolEntry } from "./mark-form"

const h = createColumnHelper<PeppolMarkRow>()
const COLS = [
  h.accessor("mark_code", { header: "Kod" }),
  h.accessor("peppol_kind", { header: "Profil" }),
  h.accessor("source_ref", { header: "Źródło" }),
]

export function PeppolDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const hasSession = Boolean(org && tenant.userId)
  const q = useQuery({
    enabled: hasSession,
    queryFn: fetchPeppolMarks,
    queryKey: ["peppol-marks", org],
    retry: false,
  })

  return (
    <div className="grid gap-5" data-peppol="page">
      <CatalogHeading
        title="Peppol + MPP"
        subtitle="EXP2.20 · peppol|mpp|as4 · bez AS4 live"
      />
      {hasSession ? <PeppolEntry organizationId={org} /> : <TenantSessionNotice />}
      {q.error ? <CatalogError error={q.error} /> : null}
      {hasSession && !q.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            peppol_kind: "Profil",
            source_ref: "Źródło",
          }}
          columns={COLS}
          data={q.data ?? []}
          globalFilterPlaceholder="Filtr Peppol…"
          tableKey={BUSINESS_LISTS.peppolMark.tableKey}
        />
      ) : null}
    </div>
  )
}
