import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildShipperBindMarkWrite, saveShipperBindMark } from "@/lib/shipper-bind-marks-api"

const KIND_RADIO = ["tender", "party", "other"] as const

export function ShipperBindMarkSave(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [markCode, setMarkCode] = useState("shipper_bind_tender_01")
  const [kind, setKind] = useState<string>("tender")
  const [origin, setOrigin] = useState("fixture://shipper-bind-mark/")
  const mutation = useMutation({
    mutationFn: () =>
      saveShipperBindMark(buildShipperBindMarkWrite(markCode, kind, origin)),
    onSuccess: () => {
      setMarkCode("shipper_bind_tender_01")
      setKind("tender")
      setOrigin("fixture://shipper-bind-mark/")
      void client.invalidateQueries({ queryKey: ["shipper-bind-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex max-w-md flex-col gap-3"
      data-shipper-bind-mark="entry"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) mutation.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance wiązania załadowcy (HITL) — bez Alpega i bez UUID FK.
      </p>
      <label className="grid gap-1 text-xs">
        mark_code (snake 2–32)
        <input
          aria-label="Kod shipper_bind_mark"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setMarkCode(change.target.value)}
          required
          value={markCode}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>bind_kind</legend>
        {KIND_RADIO.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="shipper-bind-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://shipper-bind-mark/…)"
        ariaLabel="Pochodzenie shipper_bind_mark"
        value={origin}
        onChange={setOrigin}
      />
      {mutation.error ? <CatalogError error={mutation.error} /> : null}
      <Button disabled={!props.organizationId || mutation.isPending} type="submit">
        Zapisz bind załadowcy
      </Button>
    </form>
  )
}
