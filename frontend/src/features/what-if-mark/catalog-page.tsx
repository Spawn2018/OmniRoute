import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchWhatIfMarks, type WhatIfMarkRow } from "@/lib/what-if-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { WhatIfMarkComposer } from "./mark-form"

const helper = createColumnHelper<WhatIfMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("scenario_kind", { header: "Scenariusz" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function WhatIfMarkBoard() {
  const tenant = getTenantContext()
  const orgId = tenant.organizationId
  const ready = Boolean(orgId && tenant.userId)
  const catalog = useQuery({
    enabled: ready,
    queryFn: fetchWhatIfMarks,
    queryKey: ["what-if-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-wif="board">
      <CatalogHeading
        title="What-if"
        subtitle="EXP2.10 · katalog HITL · fuel/port/bankruptcy · bez silnika scenariusza"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <WhatIfMarkComposer organizationId={orgId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {ready && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            scenario_kind: "Scenariusz",
            source_ref: "Źródło",
          }}
          columns={COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtruj scenariusze…"
          tableKey={BUSINESS_LISTS.whatIfMark.tableKey}
        />
      ) : null}
    </section>
  )
}
