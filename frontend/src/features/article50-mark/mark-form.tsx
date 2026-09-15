import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildArticle50MarkWrite,
  saveArticle50Mark,
} from "@/lib/article50-marks-api"

export function Article50MarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("a50_generated_01")
  const [kind, setKind] = useState("generated")
  const [origin, setOrigin] = useState("fixture://article50-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveArticle50Mark(buildArticle50MarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("a50_generated_01")
      setKind("generated")
      setOrigin("fixture://article50-mark/")
      void cache.invalidateQueries({
        queryKey: ["article50-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-article50-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL etykiety art. 50 (generated/exempt/human). Przebudowa U-art50, scoring
        i live LLM label zostają poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://article50-mark/…)"
        ariaLabel="Pochodzenie znacznika art. 50"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika art. 50"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Rodzaj etykiety</span>
        <select
          aria-label="Rodzaj etykiety generated exempt human other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="generated">generated — z modelu</option>
          <option value="exempt">exempt — zwolniony</option>
          <option value="human">human — człowiek</option>
          <option value="other">other — pozostałe</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz etykiete art. 50
      </Button>
    </form>
  )
}
