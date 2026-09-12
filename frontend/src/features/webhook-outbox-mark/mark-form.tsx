import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createWebhookOutboxMark,
  makeWebhookOutboxPayload,
} from "@/lib/webhook-outbox-marks-api"

const OUTBOX_KINDS = [
  { key: "webhook", tip: "webhook" },
  { key: "retry", tip: "ponowienie" },
  { key: "dead", tip: "dead letter" },
  { key: "other", tip: "inny" },
] as const

export function WebhookOutboxComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("wh_hook_01")
  const [kind, setKind] = useState("webhook")
  const [ref, setRef] = useState("fixture://webhook-outbox-mark/")
  const write = useMutation({
    mutationFn: () =>
      createWebhookOutboxMark(makeWebhookOutboxPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("wh_hook_01")
      setKind("webhook")
      setRef("fixture://webhook-outbox-mark/")
      void client.invalidateQueries({
        queryKey: ["webhook-outbox-marks", props.organizationId],
      })
    },
  })

  return (
    <div className="border-l-2 border-primary/40 pl-3" data-wh="outbox-composer">
      <h2 className="text-sm font-semibold">Znacznik webhook outbox (HITL)</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        Tryb outboxu webhooków. Bez live dispatch i bez Temporal.
      </p>
      <form
        className="grid gap-2 md:grid-cols-3"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) write.mutate()
        }}
      >
        <label className="text-xs md:col-span-1">
          mark_code
          <input
            aria-label="mark_code webhook"
            className="mt-1 h-9 w-full rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          outbox_kind
          <select
            aria-label="outbox_kind"
            className="mt-1 h-9 w-full rounded border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {OUTBOX_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <div className="text-xs">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref webhook"
            value={ref}
            onChange={setRef}
          />
        </div>
        {write.error ? (
          <div className="md:col-span-3">
            <CatalogError error={write.error} />
          </div>
        ) : null}
        <Button
          className="md:col-span-3"
          disabled={!props.organizationId || write.isPending}
          type="submit"
        >
          Zapisz znacznik webhook
        </Button>
      </form>
    </div>
  )
}
