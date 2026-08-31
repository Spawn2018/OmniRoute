import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { hitlSplitView } from "@/features/extraction/hitl-split"
import type { ExtractionDraft } from "@/lib/extractions-api"

type HitlReviewSplitProps = {
  draft: ExtractionDraft | null
  busy: boolean
  onAccept: (draftId: string) => void
  onReject: (draftId: string) => void
}

export function HitlReviewSplit({ draft, busy, onAccept, onReject }: HitlReviewSplitProps) {
  const view = hitlSplitView(draft)

  if (view.kind === "empty") {
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
        <pre className="mt-2 max-h-64 overflow-auto whitespace-pre-wrap text-xs">{view.preview}</pre>
      </section>
      <section className="min-w-0 rounded-md border border-border bg-card p-3">
        <h3 className="text-xs font-medium text-muted-foreground">Recenzja</h3>
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
        {view.unparsedRegions.length > 0 ? (
          <p className="mt-2 text-xs text-muted-foreground">
            Nierozpoznane: {view.unparsedRegions.join(" · ")}
          </p>
        ) : null}
        <div className="mt-3 flex gap-1">
          <Button
            type="button"
            size="sm"
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
