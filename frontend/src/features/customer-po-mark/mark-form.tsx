import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createCustomerPoMark,
  makeCustomerPoMarkPayload,
} from "@/lib/customer-po-marks-api"

const REF_KINDS = [
  { value: "customer_po", label: "Customer PO" },
  { value: "release", label: "Release" },
  { value: "call_off", label: "Call-off" },
  { value: "other", label: "Inne" },
] as const

export function CustomerPoMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("cpm_customer_po_01")
  const [kind, setKind] = useState("customer_po")
  const [ref, setRef] = useState("fixture://customer-po-mark/")
  const save = useMutation({
    mutationFn: () =>
      createCustomerPoMark(makeCustomerPoMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("cpm_customer_po_01")
      setKind("customer_po")
      setRef("fixture://customer-po-mark/")
      void qc.invalidateQueries({
        queryKey: ["customer-po-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-cpm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code customer po"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        ref_kind
        <select
          aria-label="ref_kind customer_po release call_off other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {REF_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref customer po"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik referencji PO klienta
      </Button>
    </form>
  )
}
