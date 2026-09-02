import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { aiProposals, fetchExtractionDrafts } from "@/lib/extractions-api"
import { getTenantContext } from "@/lib/tenant"

export function AiCopilotPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const drafts = useQuery({
    queryKey: ["ai-copilot-drafts", ctx.organizationId],
    queryFn: () => fetchExtractionDrafts("pending"),
    enabled: ready,
    retry: false,
  })
  const rows = aiProposals(drafts.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-ai-copilot="board">
      <CatalogHeading
        title="Propozycje AI"
        subtitle="ai_copilot M-57 · extraction pending · Art. 50 · nie czat · nie accept"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {drafts.isError ? <CatalogError error={drafts.error} /> : null}
      <ul>
        {rows.map((row) => (
          <li key={row.id} className="text-xs">
            {row.source_ref} {row.status}{" "}
            <Link className="underline" to="/extractions">
              HITL
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
