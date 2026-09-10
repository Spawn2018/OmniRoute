import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listCircleSims, type CircleSimRow } from "@/lib/circle-sims-api"
import { getTenantContext } from "@/lib/tenant"
import { CircleSave } from "./circle-form"

const helper = createColumnHelper<CircleSimRow>()

const columns = [
  helper.accessor("sim_code", { header: "Kod" }),
  helper.accessor("unload_unlocode", { header: "Rozładunek" }),
  helper.accessor("load_unlocode", { header: "Załadunek" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

const COLUMN_LABELS = {
  sim_code: "Kod",
  unload_unlocode: "Rozładunek",
  load_unlocode: "Załadunek",
  source_ref: "Pochodzenie",
}

function CircleRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["circle-sims", args.organizationId],
    queryFn: listCircleSims,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <div className="min-w-0 flex-1">
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <DataTableShell
        tableKey={BUSINESS_LISTS.circleSim.tableKey}
        columns={columns}
        data={listed.data ?? []}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Szukaj kółka…"
      />
    </div>
  )
}

export function CircleDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-circle-sim="desk">
      <CatalogHeading
        title="Kółko"
        subtitle="G2.20 circle_sim · para unload/load jako dane · nie silnik"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <CircleSave organizationId={ctx.organizationId} />
          <CircleRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
