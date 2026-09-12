import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useId, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildEDeliveryBody, saveEDeliveryMark } from "@/lib/e-delivery-marks-api"

const CHANNELS: ReadonlyArray<{ value: string; caption: string }> = [
  { value: "edor", caption: "skrzynka e-Doręczeń" },
  { value: "registered", caption: "list polecony" },
  { value: "receipt", caption: "potwierdzenie odbioru" },
  { value: "other", caption: "pozostały kanał" },
]

export function EDeliveryEntry(props: { organizationId: string | null }) {
  const formId = useId()
  const qc = useQueryClient()
  const [markCode, setMarkCode] = useState("edor_lane_a")
  const [channel, setChannel] = useState("edor")
  const [origin, setOrigin] = useState("tenant:manual")
  const save = useMutation({
    mutationFn: () =>
      saveEDeliveryMark(buildEDeliveryBody(markCode, channel, origin)),
    onSuccess: () => {
      setMarkCode("edor_lane_a")
      setChannel("edor")
      setOrigin("tenant:manual")
      void qc.invalidateQueries({
        queryKey: ["e-delivery-marks", props.organizationId],
      })
    },
  })

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (props.organizationId == null) return
    save.mutate()
  }

  return (
    <aside className="border-l-2 border-primary/40 pl-4" data-edor="composer">
      <form className="grid max-w-lg gap-3" id={formId} onSubmit={onSubmit}>
        <div>
          <p className="text-sm font-medium tracking-tight">Nowy kanał doręczenia</p>
          <p className="text-xs text-muted-foreground">
            Tylko HITL. Brak wywołania PUDO i brak zapisu mail_draft.
          </p>
        </div>
        <label className="grid gap-1 text-xs font-medium">
          mark_code
          <input
            aria-label="mark_code e-Doręczenia"
            className="h-9 rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setMarkCode(e.target.value)}
            required
            value={markCode}
          />
        </label>
        <fieldset className="grid gap-2">
          <legend className="text-xs font-medium">delivery_kind</legend>
          {CHANNELS.map((row) => (
            <label className="flex items-center gap-2 text-xs" key={row.value}>
              <input
                checked={channel === row.value}
                name="delivery_kind"
                onChange={() => setChannel(row.value)}
                type="radio"
                value={row.value}
              />
              <span>
                {row.value} — {row.caption}
              </span>
            </label>
          ))}
        </fieldset>
        <CatalogSourceRefField
          label="source_ref (tenant:manual albo fixture://…)"
          ariaLabel="source_ref e-Doręczenia"
          value={origin}
          onChange={setOrigin}
        />
        {save.error ? <CatalogError error={save.error} /> : null}
        <Button
          disabled={props.organizationId == null || save.isPending}
          type="submit"
        >
          Zapisz kanał
        </Button>
      </form>
    </aside>
  )
}
