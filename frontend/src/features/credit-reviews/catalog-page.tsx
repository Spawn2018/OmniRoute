import { createColumnHelper } from "@tanstack/react-table"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import * as Catalog from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  attachCreditReviewBureau,
  createCreditReview,
  creditReviewAttachBureauBody,
  creditReviewCreateBody,
  fetchCreditReviews,
  resolveCreditReview,
  type CreditReview,
} from "@/lib/credit-reviews-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<CreditReview>()

const columns = [
  helper.accessor("party_id", {
    id: "party_id",
    header: "Kontrahent",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  helper.accessor("review_date", {
    id: "review_date",
    header: "Dzień",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  helper.accessor("decision", {
    id: "decision",
    header: "Decyzja",
    cell: (info) => info.getValue(),
  }),
  helper.accessor("note", {
    id: "note",
    header: "Notatka",
    cell: (info) => info.getValue() ?? "—",
  }),
  helper.accessor("source_ref", {
    id: "source_ref",
    header: "Pochodzenie",
    cell: (info) => info.getValue(),
  }),
  helper.accessor("bureau_attachment_ref", {
    id: "bureau_attachment_ref",
    header: "Raport",
    cell: (info) => info.getValue() ?? "—",
  }),
]

const COLUMN_LABELS = {
  party_id: "party_id",
  review_date: "Dzień recenzji",
  decision: "ok / hold / refuse",
  note: "Notatka operatora",
  source_ref: "source_ref",
  bureau_attachment_ref: "wskazanie raportu",
}

function BureauAttachForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [reviewId, setReviewId] = useState("")
  const [bureauRef, setBureauRef] = useState("")
  const attachMutation = useMutation({
    mutationFn: () =>
      attachCreditReviewBureau(
        reviewId.trim(),
        creditReviewAttachBureauBody({ bureauAttachmentRef: bureauRef }),
      ),
    onSuccess: () => {
      setReviewId("")
      setBureauRef("")
      void client.invalidateQueries({ queryKey: ["credit-reviews", args.organizationId] })
    },
  })
  return (
    <form
      className="flex flex-wrap items-end gap-2 rounded-md border border-border bg-card p-3"
      onSubmit={(event) => {
        event.preventDefault()
        attachMutation.mutate()
      }}
    >
      <Input
        aria-label="Recenzja do raportu"
        placeholder="credit_review.id"
        value={reviewId}
        onChange={(event) => setReviewId(event.target.value)}
        required
      />
      <Input
        aria-label="Wskazanie raportu wywiadowni"
        placeholder="bureau_attachment_ref"
        value={bureauRef}
        onChange={(event) => setBureauRef(event.target.value)}
        required
      />
      <Button type="submit" disabled={attachMutation.isPending || !args.organizationId}>
        Dołącz raport
      </Button>
      {attachMutation.isError ? <Catalog.CatalogError error={attachMutation.error} /> : null}
    </form>
  )
}

export function CreditReviewCatalogPage() {
  const ctx = getTenantContext()
  const client = useQueryClient()
  const [partyId, setPartyId] = useState("")
  const [reviewDate, setReviewDate] = useState("")
  const [decision, setDecision] = useState("ok")
  const [note, setNote] = useState("")
  const [lookupPartyId, setLookupPartyId] = useState("")
  const [lookupDate, setLookupDate] = useState("")
  const [resolved, setResolved] = useState<CreditReview | null>(null)

  const query = useQuery({
    queryKey: ["credit-reviews", ctx.organizationId],
    queryFn: fetchCreditReviews,
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      createCreditReview(creditReviewCreateBody({ partyId, reviewDate, decision, note })),
    onSuccess: () => {
      setPartyId("")
      setReviewDate("")
      setDecision("ok")
      setNote("")
      void client.invalidateQueries({ queryKey: ["credit-reviews", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: () => resolveCreditReview(lookupPartyId.trim(), lookupDate),
    onSuccess: setResolved,
    onError: () => setResolved(null),
  })

  return (
    <div className="flex flex-col gap-3">
      <Catalog.CatalogHeading
        title="Katalog recenzji kredytowych"
        subtitle="credit_review M-14 · decyzja operatora per dzień · nie scoring"
      />

      {!ctx.organizationId || !ctx.userId ? <Catalog.TenantSessionNotice /> : null}

      <form
        className="flex flex-wrap items-end gap-2 rounded-md border border-border bg-card p-3"
        onSubmit={(event) => {
          event.preventDefault()
          createMutation.mutate()
        }}
      >
        <Input
          aria-label="Kontrahent recenzji"
          placeholder="party_id"
          value={partyId}
          onChange={(event) => setPartyId(event.target.value)}
          required
        />
        <Input
          aria-label="Dzień recenzji"
          type="date"
          value={reviewDate}
          onChange={(event) => setReviewDate(event.target.value)}
          required
        />
        <select
          aria-label="Decyzja recenzji"
          className="h-8 rounded-md border border-input bg-background px-2 text-sm"
          value={decision}
          onChange={(event) => setDecision(event.target.value)}
        >
          <option value="ok">ok</option>
          <option value="hold">hold</option>
          <option value="refuse">refuse</option>
        </select>
        <Input
          aria-label="Notatka recenzji"
          placeholder="notatka (opcjonalnie)"
          value={note}
          onChange={(event) => setNote(event.target.value)}
        />
        <Button type="submit" disabled={createMutation.isPending || !ctx.organizationId}>
          Dodaj recenzję
        </Button>
      </form>

      {createMutation.isError ? <Catalog.CatalogError error={createMutation.error} /> : null}

      <fieldset className="flex flex-wrap items-end gap-2 rounded-md border border-border bg-card p-3">
        <legend className="text-sm font-medium">Rozwiąż recenzję na dzień</legend>
        <Input
          aria-label="Sprawdź kontrahenta recenzji"
          placeholder="party_id"
          value={lookupPartyId}
          onChange={(event) => setLookupPartyId(event.target.value)}
        />
        <Input
          aria-label="Sprawdź dzień recenzji"
          type="date"
          value={lookupDate}
          onChange={(event) => setLookupDate(event.target.value)}
        />
        <Button
          type="button"
          variant="outline"
          disabled={resolveMutation.isPending || !lookupPartyId || !lookupDate}
          onClick={() => resolveMutation.mutate()}
        >
          Rozwiąż
        </Button>
        {resolved ? (
          <p className="w-full font-mono text-xs">
            {resolved.decision} · {resolved.review_date} · {resolved.source_ref}
          </p>
        ) : null}
      </fieldset>

      {resolveMutation.isError ? <Catalog.CatalogError error={resolveMutation.error} /> : null}

      <BureauAttachForm organizationId={ctx.organizationId} />

      <Catalog.CatalogLoadedTable
        tableKey={BUSINESS_LISTS.creditReviews.tableKey}
        globalFilterPlaceholder="Szukaj decyzji albo dnia recenzji…"
        columnLabels={COLUMN_LABELS}
        columns={columns}
        data={query.data}
        error={query.error}
        loading={query.isLoading}
      />
    </div>
  )
}
