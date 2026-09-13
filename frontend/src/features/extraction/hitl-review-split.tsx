import { lazy, Suspense } from "react"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { CandidatePatchForm } from "@/features/extraction/candidate-patch-form"
import { hitlGeneratedContentLabel, hitlSplitView } from "@/features/extraction/hitl-split"
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
  onAccept: (draftId: string) => void
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

  if (view.kind === "empty" || draft === null) {
    return (
      <div className="rounded-md border border-border bg-card p-3 text-sm text-muted-foreground">
        Wybierz szkic z kolejki, żeby zobaczyć podgląd i recenzję.
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
      <section className="min-w-0 rounded-md border border-border bg-card p-3">
        <h3 className="text-xs font-medium text-muted-foreground">Podgląd</h3>
        <p className="mt-1 font-mono text-xs text-muted-foreground">{view.sourceRef}</p>
        {pdfBase64 !== null && isPdfBase64(pdfBase64) ? (
          <Suspense fallback={<p className="mt-2 text-xs text-muted-foreground">Ładowanie PDF…</p>}>
            <HitlPdfViewer
              pdfBase64={pdfBase64}
              highlightTexts={view.candidates.flatMap((candidate) => [
                candidate.code,
                candidate.amount_text,
                candidate.currency,
              ])}
            />
          </Suspense>
        ) : (
          <pre className="mt-2 max-h-64 overflow-auto whitespace-pre-wrap text-xs">
            {hitlPreviewSegments(view.preview, hitlPreviewSpans(view.preview, view.candidates)).map(
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
          <h3 className="text-xs font-medium text-muted-foreground">Recenzja</h3>
          <p
            data-generated-content="ai"
            role="status"
            className="text-xs font-medium text-accent"
          >
            {hitlGeneratedContentLabel(view)}
          </p>
        </div>
        {draft.status === "pending" &&
        draft.draft_kind === "rate_line" &&
        onPatchCandidates !== undefined ? (
          <CandidatePatchForm
            draftId={view.draftId}
            candidates={view.candidates}
            disabled={busy}
            onSave={onPatchCandidates}
          />
        ) : (
          <ul className="mt-2 space-y-1 text-sm">
            {view.candidates.length === 0 ? (
              <li className="text-muted-foreground">Brak kandydatów</li>
            ) : (
              view.candidates.map((candidate) => (
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
        {view.unparsedRegions.length > 0 ? (
          <p className="mt-2 text-xs text-muted-foreground">
            Nierozpoznane: {view.unparsedRegions.join(" · ")}
          </p>
        ) : null}
        <div className="mt-3 flex gap-1">
          <Button
            type="button"
            size="sm"
            data-operator-target="accept"
            disabled={busy}
            onClick={() => onAccept(view.draftId)}
          >
            Akceptuj
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            disabled={busy}
            onClick={() => onReject(view.draftId)}
          >
            Odrzuć
          </Button>
        </div>
      </section>
    </div>
  )
}
