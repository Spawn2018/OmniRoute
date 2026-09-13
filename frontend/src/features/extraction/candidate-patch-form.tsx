import { useEffect, useState } from "react"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import type { ExtractionCandidate } from "@/lib/extractions-api"

type CandidatePatchFormProps = {
  draftId: string
  candidates: ExtractionCandidate[]
  disabled: boolean
  onSave: (draftId: string, candidates: ExtractionCandidate[]) => void
}

type CandidateField = "code" | "amount_text" | "currency" | "note"

function replaceField(
  rows: ExtractionCandidate[],
  index: number,
  field: CandidateField,
  value: string,
): ExtractionCandidate[] {
  return rows.map((row, rowIndex) => (rowIndex === index ? { ...row, [field]: value } : row))
}

function CandidatePatchRow({
  candidate,
  index,
  disabled,
  onField,
}: {
  candidate: ExtractionCandidate
  index: number
  disabled: boolean
  onField: (index: number, field: CandidateField, value: string) => void
}) {
  return (
    <li className="space-y-1 rounded-md border border-border p-2">
      <span className="font-mono text-xs">
        {candidate.code} <Money amount={candidate.amount_text} currency={candidate.currency} />
      </span>
      <div className="grid gap-1 sm:grid-cols-2">
        <Input
          aria-label={`Kod kandydata ${index + 1}`}
          disabled={disabled}
          value={candidate.code}
          onChange={(event) => onField(index, "code", event.target.value)}
        />
        <Input
          aria-label={`Kwota kandydata ${index + 1}`}
          disabled={disabled}
          value={candidate.amount_text}
          onChange={(event) => onField(index, "amount_text", event.target.value)}
        />
        <Input
          aria-label={`Waluta kandydata ${index + 1}`}
          disabled={disabled}
          value={candidate.currency}
          onChange={(event) => onField(index, "currency", event.target.value)}
        />
        <Input
          aria-label={`Notatka kandydata ${index + 1}`}
          disabled={disabled}
          value={candidate.note ?? ""}
          onChange={(event) => onField(index, "note", event.target.value)}
        />
      </div>
    </li>
  )
}

export function CandidatePatchForm({
  draftId,
  candidates,
  disabled,
  onSave,
}: CandidatePatchFormProps) {
  const [rows, setRows] = useState(candidates)
  useEffect(() => {
    setRows(candidates)
  }, [candidates, draftId])

  return (
    <div className="mt-2 space-y-2">
      <ul className="space-y-2 text-sm">
        {rows.length === 0 ? (
          <li className="text-muted-foreground">Brak kandydatów</li>
        ) : (
          rows.map((candidate, index) => (
            <CandidatePatchRow
              key={`${candidate.code}-${index}`}
              candidate={candidate}
              index={index}
              disabled={disabled}
              onField={(rowIndex, field, value) =>
                setRows((current) => replaceField(current, rowIndex, field, value))
              }
            />
          ))
        )}
      </ul>
      <Button
        type="button"
        size="sm"
        variant="outline"
        data-operator-target="patch-candidates"
        disabled={disabled}
        onClick={() => onSave(draftId, rows)}
      >
        Zapisz poprawkę
      </Button>
    </div>
  )
}
