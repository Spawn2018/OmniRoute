import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchTrackingConsents, type TrackingConsentRow } from "@/lib/tracking-consents-api"
import { getTenantContext } from "@/lib/tenant"
import { TrackingConsentSave } from "./mark-form"

const helper = createColumnHelper<TrackingConsentRow>()

const COLUMNS = [
  helper.accessor("consent_code", { header: "Kod" }),
  helper.accessor("consent_kind", { header: "Rodzaj" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

export function TrackingConsentDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchTrackingConsents,
    queryKey: ["tracking-consents", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-5" data-tracking-consent="board">
      <CatalogHeading
        title="Zgoda na śledzenie"
        subtitle="BR2.2 tracking_consent · katalog HITL · nie kolumna na kontakcie · nie live poll"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <TrackingConsentSave organizationId={orgId} /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            consent_code: "Kod",
            consent_kind: "Rodzaj",
            source_ref: "Pochodzenie",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Szukaj zgody…"
          tableKey={BUSINESS_LISTS.trackingConsent.tableKey}
        />
      ) : null}
    </section>
  )
}
