import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { persistRoutingGuide, routingGuideBody } from "@/lib/routing-guides-api"

type GuideDraft = {
  guideSlug: string
  laneText: string
  modeText: string
  originPointer: string
}

const EMPTY_GUIDE: GuideDraft = {
  guideSlug: "guide_pl_de",
  laneText: "",
  modeText: "",
  originPointer: "fixture://routing-guide/",
}

export function RoutingGuideSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_GUIDE)
  const persist = useMutation({
    mutationFn: () => persistRoutingGuide(routingGuideBody(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_GUIDE })
      void cache.invalidateQueries({ queryKey: ["routing-guides", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3"
      data-routing-guide="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Przewodnik routingu jako katalog. To nie jest blokada zlecenia (409) ani mapa.
      </p>
      <label className="grid gap-1 text-xs">
        Kod przewodnika (snake 2–32)
        <input
          aria-label="Kod przewodnika routingu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, guideSlug: change.target.value })}
          required
          value={draft.guideSlug}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Korytarz (opcjonalnie)
        <input
          aria-label="Korytarz przewodnika"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, laneText: change.target.value })}
          value={draft.laneText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Tryb (opcjonalnie)
        <input
          aria-label="Tryb przewodnika"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, modeText: change.target.value })}
          value={draft.modeText}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://routing-guide/…)"
        ariaLabel="Pochodzenie przewodnika"
        value={draft.originPointer}
        onChange={(originPointer) => setDraft({ ...draft, originPointer })}
      />
      {persist.error ? <CatalogError error={persist.error} /> : null}
      <Button disabled={!args.organizationId || persist.isPending} type="submit">
        Zapisz przewodnik routingu
      </Button>
    </form>
  )
}
