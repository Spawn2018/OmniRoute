import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listCargoCoverMarks, type CargoCoverMarkRow } from "@/lib/cargo-cover-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CargoCoverMarkForm } from "./mark-form"

const cols = createColumnHelper<CargoCoverMarkRow>()

const COLUMNS = [
  cols.accessor("mark_code", { header: "Kod" }),
  cols.accessor("cover_kind", { header: "Cover" }),
  cols.accessor("source_ref", { header: "Źródło" }),
]

export function CargoCoverMarkDesk() {
  const session = getTenantContext()
  const org = session.organizationId
  const ok = Boolean(org && session.userId)
  const query = useQuery({
    enabled: ok,
    queryFn: listCargoCoverMarks,
    queryKey: ["cargo-cover-marks", org],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-cargo-cover-mark="desk">
      <CatalogHeading
        title="Cargo cover"
        subtitle="EXP2.4 · HITL cargo_cover_mark · cover_kind jako etykieta · bez live insurance"
      />
      {!ok ? <TenantSessionNotice /> : null}
      {ok ? <CargoCoverMarkForm organizationId={org} /> : null}
      {query.error ? <CatalogError error={query.error} /> : null}
      {ok && !query.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            cover_kind: "Cover",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={query.data ?? []}
          globalFilterPlaceholder="Szukaj cover…"
          tableKey={BUSINESS_LISTS.cargoCoverMark.tableKey}
        />
      ) : null}
    </section>
  )
}
