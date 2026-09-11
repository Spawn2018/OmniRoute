import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildFerryArt9Write, createFerryArt9Mark } from "@/lib/ferry-art9-marks-api"

const KINDS = [
  { id: "rest", pl: "odpoczynek art. 9" },
  { id: "watchdog", pl: "watchdog ETA vs cutoff" },
  { id: "crossing", pl: "przeprawa" },
  { id: "other", pl: "inny" },
] as const

export function FerryArt9Writer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("rest_01")
  const [kind, setKind] = useState("rest")
  const [ref, setRef] = useState("fixture://ferry-art9-mark/")
  const save = useMutation({
    mutationFn: () => createFerryArt9Mark(buildFerryArt9Write(code, kind, ref)),
    onSuccess: () => {
      setCode("rest_01")
      setKind("rest")
      setRef("fixture://ferry-art9-mark/")
      void qc.invalidateQueries({ queryKey: ["ferry-art9-marks", props.organizationId] })
    },
  })

  function submit(event: FormEvent) {
    event.preventDefault()
    if (!props.organizationId) return
    save.mutate()
  }

  return (
    <aside className="max-w-md rounded-lg bg-muted/40 p-4" data-ferry="writer">
      <h2 className="mb-1 text-sm font-semibold">Znacznik ferry art. 9</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        HITL: odpoczynek / watchdog / przeprawa. Bez tacho DDD i bez Driver Time Solver.
      </p>
      <form className="space-y-3" onSubmit={submit}>
        <label className="grid gap-1 text-xs">
          Kod
          <input
            aria-label="Kod ferry art. 9"
            className="h-9 rounded-md border bg-background px-2 font-mono"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="grid gap-1 text-xs">
          Rodzaj (`ferry_kind`)
          <select
            aria-label="Rodzaj ferry art. 9"
            className="h-9 rounded-md border bg-background px-2"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {KINDS.map((row) => (
              <option key={row.id} value={row.id}>
                {row.id} — {row.pl}
              </option>
            ))}
          </select>
        </label>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="Pochodzenie ferry art. 9"
          value={ref}
          onChange={setRef}
        />
        {save.error ? <CatalogError error={save.error} /> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz ferry art. 9
        </Button>
      </form>
    </aside>
  )
}
