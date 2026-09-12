import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createPartnerExchangeMark,
  makePartnerExchangePayload,
} from "@/lib/partner-exchange-marks-api"

const EXCHANGE_KINDS = [
  { key: "partner", tip: "partnerska" },
  { key: "spot", tip: "spot" },
  { key: "board", tip: "tablica" },
  { key: "other", tip: "inny" },
] as const

export function PartnerExchangeComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("px_partner_01")
  const [kind, setKind] = useState("partner")
  const [ref, setRef] = useState("fixture://partner-exchange-mark/")
  const save = useMutation({
    mutationFn: () =>
      createPartnerExchangeMark(makePartnerExchangePayload(code, kind, ref)),
    onSuccess: () => {
      setCode("px_partner_01")
      setKind("partner")
      setRef("fixture://partner-exchange-mark/")
      void client.invalidateQueries({
        queryKey: ["partner-exchange-marks", props.organizationId],
      })
    },
  })

  return (
    <div className="rounded-lg bg-muted/30 p-4" data-px="composer">
      <h2 className="text-sm font-semibold">Znacznik gieldy partnerskiej (HITL)</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        Tryb gieldy. Bez live Trans.eu i bez auto-post.
      </p>
      <form
        className="flex flex-wrap gap-3"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) save.mutate()
        }}
      >
        <label className="min-w-[12rem] flex-1 text-xs">
          mark_code
          <input
            aria-label="mark_code gieldy"
            className="mt-1 h-9 w-full rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="min-w-[10rem] text-xs">
          exchange_kind
          <select
            aria-label="exchange_kind"
            className="mt-1 h-9 w-full rounded border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {EXCHANGE_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <div className="min-w-[14rem] flex-1 text-xs">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref gieldy"
            value={ref}
            onChange={setRef}
          />
        </div>
        {save.error ? <div className="w-full"><CatalogError error={save.error} /></div> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz znacznik gieldy
        </Button>
      </form>
    </div>
  )
}
