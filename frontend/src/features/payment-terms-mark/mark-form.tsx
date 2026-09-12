import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createPaymentTermsMark,
  makePaymentTermsMarkPayload,
} from "@/lib/payment-terms-marks-api"

const TERMS_KINDS = [
  { value: "net", label: "Net" },
  { value: "prepaid", label: "Prepaid" },
  { value: "other", label: "Inne" },
] as const

export function PaymentTermsMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("ptm_net_30")
  const [kind, setKind] = useState("net")
  const [ref, setRef] = useState("fixture://payment-terms-mark/")
  const save = useMutation({
    mutationFn: () =>
      createPaymentTermsMark(makePaymentTermsMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("ptm_net_30")
      setKind("net")
      setRef("fixture://payment-terms-mark/")
      void qc.invalidateQueries({
        queryKey: ["payment-terms-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-ptm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code payment terms"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        terms_kind
        <select
          aria-label="terms_kind net prepaid other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {TERMS_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref payment terms"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik warunkow platnosci
      </Button>
    </form>
  )
}
