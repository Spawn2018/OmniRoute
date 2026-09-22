import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildNetworkPrintRequirementWrite,
  saveNetworkPrintRequirement,
} from "@/lib/network-print-requirements-api"

export function NetworkPrintRequirementSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("wca_label")
  const [label, setLabel] = useState("WCA")
  const [origin, setOrigin] = useState("fixture://network-print-requirement/")
  const save = useMutation({
    mutationFn: () =>
      saveNetworkPrintRequirement(
        buildNetworkPrintRequirementWrite({ code, label, origin }),
      ),
    onSuccess: () => {
      setCode("wca_label")
      setLabel("WCA")
      setOrigin("fixture://network-print-requirement/")
      void cache.invalidateQueries({
        queryKey: ["network-print-requirements", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-network-print-requirement="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Wymóg etykiety sieci jako katalog HITL. Nie blokuje wyjazdu i nie generuje PDF.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod wymogu wydruku sieci"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Etykieta sieci (1–64)
        <input
          aria-label="Etykieta sieci"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setLabel(change.target.value)}
          required
          value={label}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://network-print-requirement/…)"
        ariaLabel="Pochodzenie wymogu wydruku sieci"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz wymóg
      </Button>
    </form>
  )
}
