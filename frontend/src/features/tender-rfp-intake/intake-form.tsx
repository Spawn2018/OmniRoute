import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { intakeWrite, listIntakeMarks, persistIntakeMark } from "@/lib/tender-rfp-intakes-api"

type IntakeDraft = {
  boardStamp: string
  codeStamp: string
  originStamp: string
}

const EMPTY_INTAKE: IntakeDraft = {
  boardStamp: "",
  codeStamp: "scope",
  originStamp: "fixture://tender-rfp-intake/",
}

function IntakeSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_INTAKE)
  const persist = useMutation({
    mutationFn: () => persistIntakeMark(intakeWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_INTAKE })
      void cache.invalidateQueries({ queryKey: ["intake-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-rfp-intake="intake-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Przyjęcie HITL przy nagłówku. Szkic LLM zostaje na `/ai`. Auto-award i TED zostają leftover.
        Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu przyjęcia RFP"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod przyjęcia
        <input
          aria-label="Kod snake przyjęcia RFP"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tender-rfp-intake/…)"
        ariaLabel="Pochodzenie zapisu przyjęcia RFP"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz przyjęcie
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function IntakeRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["intake-marks", args.organizationId],
    queryFn: listIntakeMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-rfp-intake="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.intake_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function IntakePanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <IntakeSave organizationId={args.organizationId} />
      <IntakeRows organizationId={args.organizationId} />
    </div>
  )
}
