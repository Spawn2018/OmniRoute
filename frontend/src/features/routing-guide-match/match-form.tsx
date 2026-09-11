import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createRoutingGuideMatch,
  toMatchWrite,
} from "@/lib/routing-guide-matches-api"

const KINDS = [
  { id: "guide_code_only", label: "Tylko guide_code" },
  { id: "lane_label", label: "Etykieta korytarza" },
  { id: "mode_label", label: "Etykieta mode" },
] as const

export function MatchKindWriter(props: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [slug, setSlug] = useState("match_lane_01")
  const [kind, setKind] = useState("lane_label")
  const [pointer, setPointer] = useState("fixture://routing-guide-match/")
  const mutation = useMutation({
    mutationFn: () =>
      createRoutingGuideMatch(toMatchWrite({ slug, kind, pointer })),
    onSuccess: () => {
      setSlug("match_lane_01")
      setKind("lane_label")
      setPointer("fixture://routing-guide-match/")
      void cache.invalidateQueries({
        queryKey: ["routing-guide-matches", props.organizationId],
      })
    },
  })
  return (
    <form
      className="flex max-w-md flex-col gap-3 border-l-2 border-muted pl-4"
      data-routing-guide-match="editor"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) mutation.mutate()
      }}
    >
      <p className="text-sm text-muted-foreground">
        Tryb przyszłego dopasowania jako katalog. Nie uruchamia silnika na ASN ani
        zleceniu — 409 nadal patrzy na guide_code.
      </p>
      <label className="grid gap-1 text-xs">
        Kod
        <input
          aria-label="Kod trybu dopasowania"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(event) => setSlug(event.target.value)}
          required
          value={slug}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Tryb
        <select
          aria-label="Rodzaj dopasowania przewodnika"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(event) => setKind(event.target.value)}
          value={kind}
        >
          {KINDS.map((entry) => (
            <option key={entry.id} value={entry.id}>
              {entry.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://routing-guide-match/…)"
        ariaLabel="Pochodzenie trybu dopasowania"
        value={pointer}
        onChange={setPointer}
      />
      {mutation.error ? <CatalogError error={mutation.error} /> : null}
      <Button disabled={!props.organizationId || mutation.isPending} type="submit">
        Zapisz tryb dopasowania
      </Button>
    </form>
  )
}
