import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildShipmentCloneMarkWrite,
  saveShipmentCloneMark,
} from "@/lib/shipment-clone-marks-api"

export function ShipmentCloneMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("clone_last_01")
  const [kind, setKind] = useState("last_similar")
  const [origin, setOrigin] = useState("fixture://shipment-clone-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveShipmentCloneMark(buildShipmentCloneMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("clone_last_01")
      setKind("last_similar")
      setOrigin("fixture://shipment-clone-mark/")
      void cache.invalidateQueries({
        queryKey: ["shipment-clone-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-shipment-clone-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL intencji klonu zlecenia (last_similar/manual_pick/other).
        Auto-copy i drugi SoR zostaja poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://shipment-clone-mark/…)"
        ariaLabel="Pochodzenie znacznika intencji klonu"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika intencji klonu"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Rodzaj intencji</span>
        <select
          aria-label="Rodzaj intencji klonu last_similar manual_pick other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="last_similar">last_similar — ostatnie podobne</option>
          <option value="manual_pick">manual_pick — wybor reczny</option>
          <option value="other">other — pozostale</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz intencje klonu
      </Button>
    </form>
  )
}
