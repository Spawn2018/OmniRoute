import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildHandoverNoteWrite,
  saveHandoverNote,
} from "@/lib/handover-notes-api"

export function HandoverNoteSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("shift_a_01")
  const [situation, setSituation] = useState("")
  const [background, setBackground] = useState("")
  const [assessment, setAssessment] = useState("")
  const [recommendation, setRecommendation] = useState("")
  const [origin, setOrigin] = useState("fixture://handover-note/")
  const save = useMutation({
    mutationFn: () =>
      saveHandoverNote(
        buildHandoverNoteWrite({
          code,
          situation,
          background,
          assessment,
          recommendation,
          origin,
        }),
      ),
    onSuccess: () => {
      setCode("shift_a_01")
      setSituation("")
      setBackground("")
      setAssessment("")
      setRecommendation("")
      setOrigin("fixture://handover-note/")
      void cache.invalidateQueries({
        queryKey: ["handover-notes", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-handover-note="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL wpis przekazania zmiany z czterema polami tekstu S/B/A/R. Auto z T6
        i drugi czat zostaja poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://handover-note/…)"
        ariaLabel="Pochodzenie notatki SBAR"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod notatki (snake 2–32)</span>
        <input
          aria-label="Kod notatki SBAR"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Sytuacja</span>
        <textarea
          aria-label="Sytuacja SBAR"
          className="min-h-16 rounded-none border bg-background px-2 py-1 font-mono"
          onChange={(change) => setSituation(change.target.value)}
          required
          value={situation}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Tlo</span>
        <textarea
          aria-label="Tlo SBAR"
          className="min-h-16 rounded-none border bg-background px-2 py-1 font-mono"
          onChange={(change) => setBackground(change.target.value)}
          required
          value={background}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Ocena</span>
        <textarea
          aria-label="Ocena SBAR"
          className="min-h-16 rounded-none border bg-background px-2 py-1 font-mono"
          onChange={(change) => setAssessment(change.target.value)}
          required
          value={assessment}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Rekomendacja</span>
        <textarea
          aria-label="Rekomendacja SBAR"
          className="min-h-16 rounded-none border bg-background px-2 py-1 font-mono"
          onChange={(change) => setRecommendation(change.target.value)}
          required
          value={recommendation}
        />
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz notatke SBAR
      </Button>
    </form>
  )
}
