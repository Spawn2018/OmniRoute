import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  awardReviewWrite,
  listAwardReviewMarks,
  persistAwardReviewMark,
} from "@/lib/tender-award-reviews-api"

type ReviewDraft = {
  boardStamp: string
  reviewStamp: string
  originStamp: string
}

const EMPTY_REVIEW: ReviewDraft = {
  boardStamp: "",
  reviewStamp: "countersign",
  originStamp: "fixture://tender-award-review/",
}

function AwardReviewSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_REVIEW)
  const persist = useMutation({
    mutationFn: () => persistAwardReviewMark(awardReviewWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_REVIEW })
      void cache.invalidateQueries({ queryKey: ["award-review-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-award-review="review-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Drugi podpis przy nagłówku. TED i CO₂ zostają leftover. Status nagłówka nie zmienia się tu.
        Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu przeglądu nagrody"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod przeglądu
        <select
          aria-label="Przegląd countersign challenge"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.reviewStamp}
          onChange={(change) => setDraft({ ...draft, reviewStamp: change.target.value })}
          required
        >
          <option value="countersign">countersign</option>
          <option value="challenge">challenge</option>
        </select>
      </label>
      <p className="text-xs text-muted-foreground">source_ref: tenant:manual albo fixture://tender-award-review/…</p>
      <input
        aria-label="source_ref przeglądu nagrody"
        className="h-9 max-w-lg rounded-md border bg-background px-2 font-mono text-xs"
        value={draft.originStamp}
        onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
        required
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz przegląd
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function AwardReviewRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["award-review-marks", args.organizationId],
    queryFn: listAwardReviewMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-award-review="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.review_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function AwardReviewPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <AwardReviewSave organizationId={args.organizationId} />
      <AwardReviewRows organizationId={args.organizationId} />
    </div>
  )
}
