import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildClauseWrite, saveClauseNotice } from "@/lib/clause-notices-api"

export function ClauseNoticeSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("late_delivery_01")
  const [label, setLabel] = useState("late delivery notice")
  const [origin, setOrigin] = useState("fixture://clause-notice/")
  const save = useMutation({
    mutationFn: () => saveClauseNotice(buildClauseWrite({ code, label, origin })),
    onSuccess: () => {
      setCode("late_delivery_01")
      setLabel("late delivery notice")
      setOrigin("fixture://clause-notice/")
      void cache.invalidateQueries({ queryKey: ["clause-notices", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-clause-notice="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Powiadomienie o klauzuli jako katalog HITL. Etykieta to dana, nie FK i nie 409.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod powiadomienia o klauzuli"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Etykieta klauzuli (1–128)
        <input
          aria-label="Etykieta klauzuli"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setLabel(change.target.value)}
          required
          value={label}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://clause-notice/…)"
        ariaLabel="Pochodzenie powiadomienia o klauzuli"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz powiadomienie o klauzuli
      </Button>
    </form>
  )
}
