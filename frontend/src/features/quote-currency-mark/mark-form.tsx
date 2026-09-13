import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createQuoteCurrencyMark,
  makeQuoteCurrencyMarkPayload,
} from "@/lib/quote-currency-marks-api"

const CURRENCY_KINDS = [
  { value: "account", label: "Account" },
  { value: "pay", label: "Pay" },
  { value: "other", label: "Inne" },
] as const

export function QuoteCurrencyMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("qcm_account_main")
  const [kind, setKind] = useState("account")
  const [ref, setRef] = useState("fixture://quote-currency-mark/")
  const save = useMutation({
    mutationFn: () =>
      createQuoteCurrencyMark(makeQuoteCurrencyMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("qcm_account_main")
      setKind("account")
      setRef("fixture://quote-currency-mark/")
      void qc.invalidateQueries({
        queryKey: ["quote-currency-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-qcm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code quote currency"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        currency_kind
        <select
          aria-label="currency_kind account pay other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {CURRENCY_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref quote currency"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik quote currency
      </Button>
    </form>
  )
}
