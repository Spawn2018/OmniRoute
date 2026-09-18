import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildDocumentKindMatchMarkWrite,
  saveDocumentKindMatchMark,
} from "@/lib/document-kind-match-marks-api"

const KINDS = ["exact", "alias", "missing", "other"] as const

export function DocumentKindMatchMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("match_01")
  const [kind, setKind] = useState<string>("exact")
  const [origin, setOrigin] = useState("fixture://document-kind-match-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveDocumentKindMatchMark(buildDocumentKindMatchMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("match_01")
      setKind("exact")
      setOrigin("fixture://document-kind-match-mark/")
      void cache.invalidateQueries({
        queryKey: ["document-kind-match-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-document-kind-match-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja bramy tworzenia zlecenia jako katalog HITL. Rodzaj to dana, nie live 409
        i nie egzekucja blocks_create.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika dopasowania rodzaju dokumentu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj bramy</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="create-block-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://document-kind-match-mark/…)"
        ariaLabel="Pochodzenie znacznika dopasowania rodzaju dokumentu"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz bramę
      </Button>
    </form>
  )
}
