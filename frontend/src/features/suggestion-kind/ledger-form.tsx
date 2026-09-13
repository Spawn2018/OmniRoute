import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createSuggestionKind,
  makeSuggestionKindPayload,
} from "@/lib/suggestion-kinds-api"

export function SuggestionKindComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [kindCode, setKindCode] = useState("tender_twin")
  const [ref, setRef] = useState("fixture://suggestion-kind/")
  const save = useMutation({
    mutationFn: () =>
      createSuggestionKind(
        makeSuggestionKindPayload({
          kindCode,
          sourceRef: ref,
        }),
      ),
    onSuccess: () => {
      setRef("fixture://suggestion-kind/")
      void qc.invalidateQueries({
        queryKey: ["suggestion-kinds", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-suggestion-kind="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        kind_code
        <input
          aria-label="kind_code rodzaj podpowiedzi"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setKindCode(e.target.value)}
          required
          value={kindCode}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref suggestion kind"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz rodzaj podpowiedzi
      </Button>
    </form>
  )
}
