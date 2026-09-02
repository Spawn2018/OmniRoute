import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { fetchExtractionDrafts } from "@/lib/extractions-api"
import { operatorNotices } from "@/lib/operator-notices"
import { fetchQuotations } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_QUOTE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

export function OperatorNoticePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const drafts = useQuery({
    queryKey: ["notice-drafts", ctx.organizationId],
    queryFn: () => fetchExtractionDrafts("pending"),
    enabled: ready,
    retry: false,
  })
  const quotations = useQuery({
    queryKey: ["notice-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_QUOTE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const notices = operatorNotices(drafts.data ?? [], quotations.data ?? [])
  const hasAiDraft = notices.some((row) => row.kind === "extraction_draft")

  return (
    <div className="flex flex-col gap-4" data-operator-notice="board">
      <CatalogHeading
        title="Powiadomienia"
        subtitle="operator_notice M-34 · praca do zrobienia · nie wysyłka · nie tabela"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {drafts.isError ? <CatalogError error={drafts.error} /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      {hasAiDraft ? (
        <p className="text-xs text-muted-foreground">system AI · recenzja człowieka (Art. 50)</p>
      ) : null}
      {notices.map((row) => (
        <p key={`${row.kind}:${row.id}`} className="text-xs">
          <Link className="underline" to={row.href}>
            {row.kind} {row.label}
          </Link>
          {row.amount !== null && row.currency !== null ? (
            <>
              {" "}
              <Money amount={row.amount} currency={row.currency} />
            </>
          ) : null}
        </p>
      ))}
    </div>
  )
}
