import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildShipperLikeMarkWrite, saveShipperLikeMark } from "@/lib/shipper-like-marks-api"

const LIKE_KINDS = ["match", "gap", "bench", "other"] as const

export function ShipperLikeMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [markCode, setMarkCode] = useState("slm_match_01")
  const [likeKind, setLikeKind] = useState<string>("match")
  const [sourceRef, setSourceRef] = useState("fixture://shipper-like-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveShipperLikeMark(
        buildShipperLikeMarkWrite({ code: markCode, kind: likeKind, origin: sourceRef }),
      ),
    onSuccess: () => {
      setMarkCode("slm_match_01")
      setLikeKind("match")
      setSourceRef("fixture://shipper-like-mark/")
      void cache.invalidateQueries({ queryKey: ["shipper-like-marks", args.organizationId] })
    },
  })
  function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (!args.organizationId) return
    save.mutate()
  }
  return (
    <form className="grid max-w-xl gap-3" data-shipper-like-mark="write" onSubmit={onSubmit}>
      <p className="text-xs text-muted-foreground">
        Stance like-for-like jako katalog HITL. To etykieta porównania, nie SQL i nie Alpega.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod stance like-for-like"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setMarkCode(change.target.value)}
          required
          value={markCode}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Stance</legend>
        {LIKE_KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={likeKind === token}
              name="shipper-like-mark-kind"
              onChange={() => setLikeKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://shipper-like-mark/…)"
        ariaLabel="Pochodzenie stance like-for-like"
        value={sourceRef}
        onChange={setSourceRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stance
      </Button>
    </form>
  )
}
