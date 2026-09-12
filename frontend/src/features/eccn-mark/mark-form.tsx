import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createEccnMark, makeEccnPayload } from "@/lib/eccn-marks-api"

const CONTROL = [
  { key: "eccn", hint: "numer ECCN" },
  { key: "ear", hint: "EAR" },
  { key: "license", hint: "licencja" },
  { key: "other", hint: "inny" },
] as const

export function EccnComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("eccn_ear_01")
  const [kind, setKind] = useState("eccn")
  const [ref, setRef] = useState("fixture://eccn-mark/")
  const save = useMutation({
    mutationFn: () => createEccnMark(makeEccnPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("eccn_ear_01")
      setKind("eccn")
      setRef("fixture://eccn-mark/")
      void client.invalidateQueries({ queryKey: ["eccn-marks", props.organizationId] })
    },
  })
  return (
    <div className="border-l-2 border-foreground/20 pl-3" data-eccn="composer">
      <h2 className="text-sm font-semibold">Znacznik ECCN (HITL)</h2>
      <p className="mb-2 text-xs text-muted-foreground">
        Kontrola eksportu. Bez ECCN live i bez license HTTP.
      </p>
      <form
        className="grid max-w-xl gap-2"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) save.mutate()
        }}
      >
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code ECCN"
            className="mt-1 h-9 w-full rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          control_kind
          <select
            aria-label="control_kind"
            className="mt-1 h-9 w-full rounded border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {CONTROL.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.hint}
              </option>
            ))}
          </select>
        </label>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref ECCN"
          value={ref}
          onChange={setRef}
        />
        {save.error ? <CatalogError error={save.error} /> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz znacznik ECCN
        </Button>
      </form>
    </div>
  )
}
