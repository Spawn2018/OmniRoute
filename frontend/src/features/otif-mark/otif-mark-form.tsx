import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { otifMarkBody, persistOtifMark } from "@/lib/otif-marks-api"

type MarkDraft = {
  markSlug: string
  scopeKind: string
  originPointer: string
}

const EMPTY_MARK: MarkDraft = {
  markSlug: "otif_pickup_pl",
  scopeKind: "pickup",
  originPointer: "fixture://otif-mark/",
}

export function OtifMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_MARK)
  const persist = useMutation({
    mutationFn: () => persistOtifMark(otifMarkBody(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_MARK })
      void cache.invalidateQueries({ queryKey: ["otif-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3"
      data-otif-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Zakres OTIF jako katalog. To nie jest wyliczanie procentu ani scoring SQL.
      </p>
      <label className="grid gap-1 text-xs">
        Kod znacznika (snake 2–32)
        <input
          aria-label="Kod znacznika OTIF"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, markSlug: change.target.value })}
          required
          value={draft.markSlug}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Zakres (pickup / delivery / sku)
        <select
          aria-label="Zakres OTIF"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, scopeKind: change.target.value })}
          value={draft.scopeKind}
        >
          <option value="pickup">pickup</option>
          <option value="delivery">delivery</option>
          <option value="sku">sku</option>
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://otif-mark/…)"
        ariaLabel="Pochodzenie znacznika OTIF"
        value={draft.originPointer}
        onChange={(originPointer) => setDraft({ ...draft, originPointer })}
      />
      {persist.error ? <CatalogError error={persist.error} /> : null}
      <Button disabled={!args.organizationId || persist.isPending} type="submit">
        Zapisz znacznik OTIF
      </Button>
    </form>
  )
}
