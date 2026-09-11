import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchRegistryPollMarks, type RegistryPollMarkRow } from "@/lib/registry-poll-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { RegistryPollMarkSave } from "./mark-form"

const helper = createColumnHelper<RegistryPollMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("poll_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function RegistryPollMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchRegistryPollMarks,
    queryKey: ["registry-poll-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-registry-poll-mark="board">
      <CatalogHeading
        title="Poll rejestrów"
        subtitle="EXP7.2 registry_poll_mark · katalog HITL · nie live scrape · nie notice auto"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <RegistryPollMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            poll_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj poll…"
          tableKey={BUSINESS_LISTS.registryPollMark.tableKey}
        />
      ) : null}
    </section>
  )
}
