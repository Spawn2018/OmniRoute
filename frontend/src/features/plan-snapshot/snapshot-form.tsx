import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { persistSnapshot, snapshotWrite } from "@/lib/plan-snapshots-api"

type SnapshotDraft = {
  codeStamp: string
  shipmentStamp: string
  tripStamp: string
  resourceStamp: string
  authorStamp: string
  whenStamp: string
  originStamp: string
}

const EMPTY_SNAPSHOT: SnapshotDraft = {
  codeStamp: "plan_v1",
  shipmentStamp: "",
  tripStamp: "",
  resourceStamp: "",
  authorStamp: "Anna",
  whenStamp: "2026-09-10T12:00:00+02:00",
  originStamp: "fixture://plan-snapshot/",
}

export function SnapshotSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SNAPSHOT)
  const persist = useMutation({
    mutationFn: () => persistSnapshot(snapshotWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_SNAPSHOT })
      void cache.invalidateQueries({ queryKey: ["plan-snapshots", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-plan-snapshot="snapshot-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Wersja planu jako dane: kod, trójka UUID (zlecenie / przejazd / zasób), autor i czas.
        Serwis nie czyta tych obiektów i nie liczy km. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod migawki (snake 2–32)
        <input
          aria-label="Kod migawki"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        UUID zlecenia (dane, bez FK)
        <input
          aria-label="UUID zlecenia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.shipmentStamp}
          onChange={(change) => setDraft({ ...draft, shipmentStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        UUID przejazdu (dane, bez FK)
        <input
          aria-label="UUID przejazdu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.tripStamp}
          onChange={(change) => setDraft({ ...draft, tripStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        UUID zasobu (dane, bez FK)
        <input
          aria-label="UUID zasobu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.resourceStamp}
          onChange={(change) => setDraft({ ...draft, resourceStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Autor (1–64)
        <input
          aria-label="Autor migawki"
          className="h-9 rounded-md border bg-background px-2"
          value={draft.authorStamp}
          onChange={(change) => setDraft({ ...draft, authorStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Czas zapisu (ISO ze strefą)
        <input
          aria-label="Czas migawki"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.whenStamp}
          onChange={(change) => setDraft({ ...draft, whenStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://plan-snapshot/…)"
        ariaLabel="source_ref migawki planu"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz migawkę
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
