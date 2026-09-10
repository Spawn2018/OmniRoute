import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { persistVisibilityConnector, visibilityFixtureBody } from "@/lib/visibility-connectors-api"

type VisibilityDraft = {
  deskSlug: string
  vendorToken: string
  originPointer: string
}

const EMPTY_FIXTURE: VisibilityDraft = {
  deskSlug: "p44_desk_pl",
  vendorToken: "p44",
  originPointer: "fixture://visibility/",
}

export function VisibilityConnectorSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_FIXTURE)
  const persist = useMutation({
    mutationFn: () => persistVisibilityConnector(visibilityFixtureBody(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_FIXTURE })
      void cache.invalidateQueries({ queryKey: ["visibility-fixtures", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3"
      data-visibility-fixture="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Fixture vendora widoczności: kod snake i token `p44`. To nie jest live track i nie
        przyjmuje klucza API.
      </p>
      <label className="grid gap-1 text-xs">
        Kod konektora widoczności (snake 2–32)
        <input
          aria-label="Kod konektora widoczności"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, deskSlug: change.target.value })}
          required
          value={draft.deskSlug}
        />
      </label>
      <fieldset className="grid gap-1 text-xs">
        <legend>Vendor (jedyny token w tym katalogu)</legend>
        <label className="flex items-center gap-2 font-mono">
          <input
            aria-label="Vendor p44"
            checked={draft.vendorToken === "p44"}
            name="visibility-vendor"
            onChange={() => setDraft({ ...draft, vendorToken: "p44" })}
            type="radio"
            value="p44"
          />
          p44
        </label>
      </fieldset>
      <label className="grid gap-1 text-xs">
        Pochodzenie (`tenant:manual` albo `fixture://visibility/…`)
        <input
          aria-label="Pochodzenie konektora widoczności"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, originPointer: change.target.value })}
          required
          value={draft.originPointer}
        />
      </label>
      <Button disabled={persist.isPending || !args.organizationId} type="submit">
        Zapisz konektor widoczności
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
