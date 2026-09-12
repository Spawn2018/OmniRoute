import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createPoSkuMark,
  makePoSkuMarkPayload,
} from "@/lib/po-sku-marks-api"

const SKU_KINDS = [
  { value: "sku", label: "SKU" },
  { value: "gtin", label: "GTIN" },
  { value: "customer_sku", label: "SKU klienta" },
  { value: "other", label: "Inne" },
] as const

export function PoSkuMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("psm_sku_01")
  const [kind, setKind] = useState("sku")
  const [ref, setRef] = useState("fixture://po-sku-mark/")
  const save = useMutation({
    mutationFn: () =>
      createPoSkuMark(makePoSkuMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("psm_sku_01")
      setKind("sku")
      setRef("fixture://po-sku-mark/")
      void qc.invalidateQueries({
        queryKey: ["po-sku-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-psm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code po sku"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        sku_kind
        <select
          aria-label="sku_kind sku gtin customer_sku other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {SKU_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref po sku"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik po sku
      </Button>
    </form>
  )
}
