import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createJitJisMark,
  makeJitJisPayload,
} from "@/lib/jit-jis-marks-api"

const FLOW_KINDS = [
  { key: "jit", tip: "JIT" },
  { key: "jis", tip: "JIS" },
  { key: "kanban", tip: "kanban" },
  { key: "other", tip: "inny" },
] as const

export function JitJisComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("jj_jit_01")
  const [kind, setKind] = useState("jit")
  const [ref, setRef] = useState("fixture://jit-jis-mark/")
  const save = useMutation({
    mutationFn: () => createJitJisMark(makeJitJisPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("jj_jit_01")
      setKind("jit")
      setRef("fixture://jit-jis-mark/")
      void client.invalidateQueries({
        queryKey: ["jit-jis-marks", props.organizationId],
      })
    },
  })

  return (
    <div className="rounded-md border border-primary/20 p-3" data-jj="composer">
      <h2 className="text-sm font-semibold">Znacznik JIT/JIS (HITL)</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        Tryb przeplywu. Bez WMS live i bez silnika JIT.
      </p>
      <form
        className="flex flex-col gap-2 sm:flex-row sm:flex-wrap"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) save.mutate()
        }}
      >
        <label className="min-w-[10rem] flex-1 text-xs">
          mark_code
          <input
            aria-label="mark_code JIT"
            className="mt-1 h-9 w-full rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="min-w-[8rem] text-xs">
          flow_kind
          <select
            aria-label="flow_kind"
            className="mt-1 h-9 w-full rounded border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {FLOW_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <div className="min-w-[12rem] flex-1 text-xs">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref JIT"
            value={ref}
            onChange={setRef}
          />
        </div>
        {save.error ? <div className="w-full"><CatalogError error={save.error} /></div> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz znacznik JIT/JIS
        </Button>
      </form>
    </div>
  )
}
