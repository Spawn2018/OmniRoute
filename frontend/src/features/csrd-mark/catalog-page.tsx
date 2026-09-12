import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadCsrdMarks, type CsrdMarkRow } from "@/lib/csrd-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CsrdMarkComposer } from "./mark-form"

const helper = createColumnHelper<CsrdMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("report_kind", { header: "Rodzaj raportu" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function CsrdMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const canLoad = Boolean(orgId && ctx.userId)
  const query = useQuery({
    enabled: canLoad,
    queryFn: loadCsrdMarks,
    queryKey: ["csrd-marks", orgId],
    retry: false,
  })
  const marks = query.data ?? []
  const showTable = canLoad && query.error == null

  return (
    <section
      className="space-y-5 rounded-md border border-emerald-900/15 bg-emerald-50/30 p-4 dark:bg-emerald-950/20"
      data-csrd="board"
    >
      <CatalogHeading
        title="Katalog CSRD / ESRS"
        subtitle="EXP3.14 · report_kind csrd|esrs|assurance|other · bez kg i live filing"
      />
      <p className="text-xs leading-relaxed text-muted-foreground">
        Znacznik rodzaju raportu ESG. Nie liczy tCO2e i nie składa filingów.
      </p>
      {!canLoad ? <TenantSessionNotice /> : <CsrdMarkComposer organizationId={orgId} />}
      {query.error ? <CatalogError error={query.error} /> : null}
      {showTable && marks.length === 0 ? (
        <p className="rounded border border-dashed p-2 text-sm text-muted-foreground">
          Brak znaczników CSRD — dodaj pierwszy wpis HITL.
        </p>
      ) : null}
      {showTable ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            report_kind: "Rodzaj raportu",
            source_ref: "Źródło",
          }}
          columns={COLS}
          data={marks}
          globalFilterPlaceholder="Filtr CSRD…"
          tableKey={BUSINESS_LISTS.csrdMark.tableKey}
        />
      ) : null}
    </section>
  )
}
