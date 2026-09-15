import { lazy, Suspense, useEffect, useState } from "react"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { CandidatePatchForm } from "@/features/extraction/candidate-patch-form"
import {
  hitlGeneratedContentLabel,
  hitlSplitView,
  draftAllowsCandidatePatch,
  bulkAcceptBlocked,
} from "@/features/extraction/hitl-split"
import {
  hitlPreviewSegments,
  hitlPreviewSpans,
  isPdfBase64,
} from "@/features/extraction/hitl-spans"
import type { ExtractionCandidate, ExtractionDraft } from "@/lib/extractions-api"

const HitlPdfViewer = lazy(() => import("@/features/extraction/hitl-pdf-viewer"))

type HitlReviewSplitProps = {
  draft: ExtractionDraft | null
  pdfBase64: string | null
  busy: boolean
  onAccept: (draftId: string, candidateIndexes?: number[]) => void
  onReject: (draftId: string) => void
  onPatchCandidates?: (draftId: string, candidates: ExtractionCandidate[]) => void
}

export function HitlReviewSplit({
  draft,
  pdfBase64,
  busy,
  onAccept,
  onReject,
  onPatchCandidates,
}: HitlReviewSplitProps) {
  const view = hitlSplitView(draft)
  const [selected, setSelected] = useState<number[]>([])

  useEffect(() => {
    if (draft === null) {
      setSelected([])
      return
    }
    setSelected(draft.payload.candidates.map((_, index) => index))
  }, [draft?.id, draft?.payload.candidates.length, draft?.payload.revision])

  if (view.kind === "empty" || draft === null) {
    return (
      <div className="rounded-md border border-border bg-card p-3 text-sm text-muted-foreground">
        Wybierz szkic z kolejki, żeby zobaczyć podgląd i recenzję.
      </div>
    )
  }

  const review = view

  const selectedCandidates = selected
    .filter((index) => index >= 0 && index < review.candidates.length)
    .map((index) => review.candidates[index])
  const acceptBlocked =
    draft.status === "pending" &&
    selectedCandidates.length > 0 &&
    bulkAcceptBlocked(selectedCandidates)
  const noSelection = draft.status === "pending" && selectedCandidates.length === 0

  function toggleIndex(index: number) {
    setSelected((current) =>
      current.includes(index)
        ? current.filter((row) => row !== index)
        : [...current, index].sort((left, right) => left - right),
    )
  }

  function submitAccept() {
    const allSelected =
      selected.length === review.candidates.length &&
      review.candidates.every((_, index) => selected.includes(index))
    onAccept(review.draftId, allSelected ? undefined : selected)
  }

  return (
    <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
      <section className="min-w-0 rounded-md border border-border bg-card p-3">
        <h3 className="text-xs font-medium text-muted-foreground">Podgląd</h3>
        <p className="mt-1 font-mono text-xs text-muted-foreground">{review.sourceRef}</p>
        {pdfBase64 !== null && isPdfBase64(pdfBase64) ? (
          <Suspense fallback={<p className="mt-2 text-xs text-muted-foreground">Ładowanie PDF…</p>}>
            <HitlPdfViewer
              pdfBase64={pdfBase64}
              highlightTexts={review.candidates.flatMap((candidate) => [
                candidate.code,
                candidate.amount_text,
                candidate.currency,
              ])}
            />
          </Suspense>
        ) : (
          <pre className="mt-2 max-h-64 overflow-auto whitespace-pre-wrap text-xs">
            {hitlPreviewSegments(review.preview, hitlPreviewSpans(review.preview, review.candidates)).map(
              (segment, index) =>
                segment.highlight ? (
                  <mark key={`${segment.text}-${index}`} data-hitl-span="text">
                    {segment.text}
                  </mark>
                ) : (
                  <span key={`${segment.text}-${index}`}>{segment.text}</span>
                ),
            )}
          </pre>
        )}
      </section>
      <section className="min-w-0 rounded-md border border-border bg-card p-3">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h3 className="text-xs font-medium text-muted-foreground">
            Recenzja · wersja {review.revision} · {review.extractPath}
          </h3>
          <p
            data-generated-content="ai"
            role="status"
            className="text-xs font-medium text-accent"
          >
            {hitlGeneratedContentLabel(review)}
          </p>
        </div>
        {review.history.length > 0 ? (
          <ul className="mt-2 space-y-1 text-xs text-muted-foreground" data-testid="extraction-history">
            {review.history.map((entry) => (
              <li key={entry.revision}>
                wersja {entry.revision}: {entry.candidateCount} kandydatów
              </li>
            ))}
          </ul>
        ) : null}
        {draft.status === "pending" &&
        draftAllowsCandidatePatch(draft.draft_kind) &&
        onPatchCandidates !== undefined ? (
          <CandidatePatchForm
            draftId={review.draftId}
            candidates={review.candidates}
            disabled={busy}
            onSave={onPatchCandidates}
          />
        ) : (
          <ul className="mt-2 space-y-1 text-sm">
            {review.candidates.length === 0 ? (
              <li className="text-muted-foreground">Brak kandydatów</li>
            ) : (
              review.candidates.map((candidate) => (
                <li key={`${candidate.code}-${candidate.amount_text}-${candidate.currency}`}>
                  <span className="font-mono text-xs">
                    {candidate.code}{" "}
                    <Money amount={candidate.amount_text} currency={candidate.currency} />
                  </span>
                </li>
              ))
            )}
          </ul>
        )}
        {draft.status === "pending" && draft.draft_kind === "rate_line" && review.candidates.length > 0 ? (
          <ul className="mt-2 space-y-1 text-xs" data-testid="accept-candidate-select">
            {review.candidates.map((candidate, index) => (
              <li key={`pick-${candidate.code}-${index}`}>
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={selected.includes(index)}
                    disabled={busy}
                    onChange={() => toggleIndex(index)}
                  />
                  <span className="font-mono">
                    {candidate.code} {candidate.amount_text} {candidate.currency}
                  </span>
                </label>
              </li>
            ))}
          </ul>
        ) : null}
        {review.unparsedRegions.length > 0 ? (
          <p className="mt-2 text-xs text-muted-foreground">
            Nierozpoznane: {review.unparsedRegions.join(" · ")}
          </p>
        ) : null}
        {acceptBlocked ? (
          <p className="mt-2 text-xs text-destructive" role="status">
            Akceptacja zbiorcza zablokowana: któryś zaznaczony kandydat ma pewność poniżej 0,70.
            Podnieś pewność albo zaznacz jednego kandydata.
          </p>
        ) : null}
        <div className="mt-3 flex gap-1">
          <Button
            type="button"
            size="sm"
            data-operator-target="accept"
            disabled={busy || acceptBlocked || noSelection}
            onClick={submitAccept}
          >
            Akceptuj
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            disabled={busy}
            onClick={() => onReject(review.draftId)}
          >
            Odrzuć
          </Button>
        </div>
      </section>
    </div>
  )
}
