import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useId, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createTenderDeclineReason,
  makeTenderDeclineReasonPayload,
} from "@/lib/tender-decline-reasons-api"

type KindOption = { value: string; pl: string; en: string }

const KIND_OPTIONS: readonly KindOption[] = [
  { value: "decline", pl: "odmowa", en: "decline" },
  { value: "no_bid", pl: "bez oferty", en: "no-bid" },
  { value: "withdraw", pl: "wycofanie", en: "withdraw" },
  { value: "other", pl: "inne", en: "other" },
]

const DEFAULTS = {
  code: "tdr_manual_01",
  kind: "decline",
  ref: "fixture://tender-decline-reason/",
} as const

export function TenderDeclineReasonComposer(props: { organizationId: string | null }) {
  const formId = useId()
  const queryClient = useQueryClient()
  const [markCode, setMarkCode] = useState<string>(DEFAULTS.code)
  const [declineKind, setDeclineKind] = useState<string>(DEFAULTS.kind)
  const [sourceRef, setSourceRef] = useState<string>(DEFAULTS.ref)

  const mutation = useMutation({
    mutationFn: async () => {
      const payload = makeTenderDeclineReasonPayload(markCode, declineKind, sourceRef)
      return createTenderDeclineReason(payload)
    },
    onSuccess: async () => {
      setMarkCode(DEFAULTS.code)
      setDeclineKind(DEFAULTS.kind)
      setSourceRef(DEFAULTS.ref)
      await queryClient.invalidateQueries({
        queryKey: ["tender-decline-reasons", props.organizationId],
      })
    },
  })

  const blocked = !props.organizationId || mutation.isPending

  return (
    <aside
      aria-labelledby={`${formId}-title`}
      className="space-y-3 border-y border-rose-900/20 py-3"
      data-tdr="composer"
    >
      <div>
        <h2 className="text-sm font-semibold tracking-tight" id={`${formId}-title`}>
          Nowy powod decline
        </h2>
        <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
          Zapis HITL. Zakaz: decline auto, RFP scrape, auto-award, kwota.
        </p>
      </div>
      <form
        className="flex flex-col gap-3"
        onSubmit={(event: FormEvent<HTMLFormElement>) => {
          event.preventDefault()
          if (!blocked) mutation.mutate()
        }}
      >
        <div className="flex flex-col gap-3 md:flex-row">
          <label className="flex min-w-0 flex-1 flex-col gap-1 text-[11px] font-medium">
            mark_code
            <input
              aria-label="mark_code tender decline"
              className="h-9 rounded-md border bg-background px-2 font-mono text-sm"
              onChange={(event) => setMarkCode(event.target.value)}
              required
              value={markCode}
            />
          </label>
          <label className="flex min-w-0 flex-1 flex-col gap-1 text-[11px] font-medium">
            decline_kind
            <select
              aria-label="decline_kind tender decline"
              className="h-9 rounded-md border bg-background px-2 text-sm"
              onChange={(event) => setDeclineKind(event.target.value)}
              value={declineKind}
            >
              {KIND_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.value} — {option.pl} / {option.en}
                </option>
              ))}
            </select>
          </label>
        </div>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref tender decline"
          value={sourceRef}
          onChange={setSourceRef}
        />
        {mutation.error ? <CatalogError error={mutation.error} /> : null}
        <div className="flex items-center gap-3">
          <Button disabled={blocked} type="submit">
            Zapisz powod decline
          </Button>
          <span className="text-[11px] text-muted-foreground">
            {mutation.isPending ? "Zapis…" : "Jednorazowy INSERT"}
          </span>
        </div>
      </form>
    </aside>
  )
}
