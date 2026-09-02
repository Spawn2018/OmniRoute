import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchExtractionDrafts, qualityGaps } from "@/lib/extractions-api"
import { t } from "@/lib/i18n"
import { getTenantContext } from "@/lib/tenant"

export function ExtractionQualityPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const drafts = useQuery({
    queryKey: ["extraction-quality-drafts", ctx.organizationId],
    queryFn: () => fetchExtractionDrafts("pending"),
    enabled: ready,
    retry: false,
  })
  const rows = qualityGaps(drafts.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-extraction-quality="board">
      <CatalogHeading
        title={t("extraction_quality.title")}
        subtitle={t("extraction_quality.subtitle")}
      />
      {!ready ? <TenantSessionNotice /> : null}
      {drafts.isError ? <CatalogError error={drafts.error} /> : null}
      <ul>
        {rows.map((row) => (
          <li key={row.id} className="text-xs">
            {row.source_ref} {row.payload.unparsed_regions.join(" ")}{" "}
            <Link className="underline" to="/extractions">
              HITL
            </Link>{" "}
            <Link className="underline" to="/ai">
              AI
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
