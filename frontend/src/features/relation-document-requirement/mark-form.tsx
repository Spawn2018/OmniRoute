import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildRelationDocumentRequirementWrite,
  saveRelationDocumentRequirement,
} from "@/lib/relation-document-requirements-api"

const KINDS = ["domestic", "international", "waste", "other"] as const

export function RelationDocumentRequirementSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("req_01")
  const [kind, setKind] = useState<string>("domestic")
  const [origin, setOrigin] = useState("fixture://relation-document-requirement/")
  const save = useMutation({
    mutationFn: () =>
      saveRelationDocumentRequirement(buildRelationDocumentRequirementWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("req_01")
      setKind("domestic")
      setOrigin("fixture://relation-document-requirement/")
      void cache.invalidateQueries({
        queryKey: ["relation-document-requirements", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-relation-document-requirement="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja wymogu dokumentow relacji (domestic/international/waste) jako katalog HITL. Rodzaj to dana, nie
        409 na shipment i nie blocks_create.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika wymogu dokumentow relacji"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj relacji</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="relation-document-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://relation-document-requirement/…)"
        ariaLabel="Pochodzenie znacznika wymogu dokumentow relacji"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz wymog
      </Button>
    </form>
  )
}
