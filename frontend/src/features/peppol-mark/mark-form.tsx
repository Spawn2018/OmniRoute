import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { postPeppolMark, toPeppolCreate } from "@/lib/peppol-marks-api"

const KIND_OPTIONS = [
  ["peppol", "sieć Peppol"],
  ["mpp", "MPP"],
  ["as4", "profil AS4"],
  ["other", "inny"],
] as const

export function PeppolEntry(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("peppol_as4_01")
  const [kind, setKind] = useState<string>("peppol")
  const [ref, setRef] = useState("fixture://peppol-mark/")
  const mutation = useMutation({
    mutationFn: () => postPeppolMark(toPeppolCreate(code, kind, ref)),
    onSuccess: () => {
      setCode("peppol_as4_01")
      setKind("peppol")
      setRef("fixture://peppol-mark/")
      void qc.invalidateQueries({ queryKey: ["peppol-marks", props.organizationId] })
    },
  })

  return (
    <section className="bg-muted/40 p-3" data-peppol="form">
      <form
        className="flex flex-wrap items-end gap-3"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) mutation.mutate()
        }}
      >
        <div className="min-w-[12rem] grow basis-40">
          <p className="mb-1 text-xs font-semibold uppercase tracking-wide">Peppol / MPP</p>
          <p className="mb-2 text-[11px] text-muted-foreground">
            HITL katalog. Zero AS4 i zero KSeF.
          </p>
          <label className="block text-[11px]">
            Kod
            <input
              aria-label="Kod Peppol"
              className="mt-1 h-8 w-full rounded border bg-background px-2 font-mono text-xs"
              onChange={(e) => setCode(e.target.value)}
              required
              value={code}
            />
          </label>
        </div>
        <label className="block text-[11px]">
          peppol_kind
          <select
            aria-label="peppol_kind"
            className="mt-1 h-8 rounded border bg-background px-2 text-xs"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {KIND_OPTIONS.map(([id, label]) => (
              <option key={id} value={id}>
                {id} ({label})
              </option>
            ))}
          </select>
        </label>
        <div className="min-w-[14rem] grow basis-48">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref Peppol"
            value={ref}
            onChange={setRef}
          />
        </div>
        {mutation.error ? <CatalogError error={mutation.error} /> : null}
        <Button
          className="h-8"
          disabled={!props.organizationId || mutation.isPending}
          size="sm"
          type="submit"
        >
          Dodaj
        </Button>
      </form>
    </section>
  )
}
