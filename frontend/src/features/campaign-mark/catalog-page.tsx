import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCampaignMarks, type CampaignMarkRow } from "@/lib/campaign-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { CampaignMarkSave } from "./mark-form"

const helper = createColumnHelper<CampaignMarkRow>()

const COLUMNS = [
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("campaign_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function CampaignMarkDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchCampaignMarks,
    queryKey: ["campaign-marks", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-campaign-mark="board">
      <CatalogHeading
        title="Kampania marketingowa"
        subtitle="BR6.5 campaign_mark · katalog HITL · nie lejek X7 · nie atrybucja live"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <CampaignMarkSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            campaign_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj kampanii…"
          tableKey={BUSINESS_LISTS.campaignMark.tableKey}
        />
      ) : null}
    </section>
  )
}
