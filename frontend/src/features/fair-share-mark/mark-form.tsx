import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import {
  CatalogError,
  CatalogSourceRefField,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createFairShareMark,
  makeFairSharePayload,
} from "@/lib/fair-share-marks-api"

const SHARE_OPTIONS = [
  { value: "fair", note: "rowny udzial" },
  { value: "split", note: "podzial" },
  { value: "pool", note: "pula" },
  { value: "other", note: "inny tryb" },
] as const

export function FairShareComposer(props: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [slug, setSlug] = useState("fs_fair_01")
  const [mode, setMode] = useState("fair")
  const [origin, setOrigin] = useState("fixture://fair-share-mark/")
  const write = useMutation({
    mutationFn: () =>
      createFairShareMark(makeFairSharePayload(slug, mode, origin)),
    onSuccess: () => {
      setSlug("fs_fair_01")
      setMode("fair")
      setOrigin("fixture://fair-share-mark/")
      void cache.invalidateQueries({
        queryKey: ["fair-share-marks", props.organizationId],
      })
    },
  })

  function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (props.organizationId) write.mutate()
  }

  return (
    <aside className="rounded border p-3" data-fs="writer">
      <p className="text-sm font-medium">Nowy znacznik fair share</p>
      <p className="mb-2 text-xs text-muted-foreground">
        Fair share HITL. Bez allocation SQL i bez drugiej marzy.
      </p>
      <form className="flex flex-col gap-3" onSubmit={onSubmit}>
        <label className="flex flex-col gap-1 text-xs">
          Kod (snake)
          <input
            aria-label="mark_code fair share"
            className="h-9 rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setSlug(e.target.value)}
            required
            value={slug}
          />
        </label>
        <label className="flex flex-col gap-1 text-xs">
          share_kind
          <select
            aria-label="share_kind"
            className="h-9 rounded border bg-background px-2 text-sm"
            onChange={(e) => setMode(e.target.value)}
            value={mode}
          >
            {SHARE_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.value} ({opt.note})
              </option>
            ))}
          </select>
        </label>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref fair share"
          value={origin}
          onChange={setOrigin}
        />
        {write.error ? <CatalogError error={write.error} /> : null}
        <Button disabled={!props.organizationId || write.isPending} type="submit">
          Zapisz znacznik fair share
        </Button>
      </form>
    </aside>
  )
}
