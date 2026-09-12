import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createDemoWipeMark,
  makeDemoWipeMarkPayload,
} from "@/lib/demo-wipe-marks-api"

const WIPE_KINDS = [
  { value: "usun", label: "Usuń (USUN)" },
  { value: "retain", label: "Zachowaj" },
  { value: "other", label: "Inne" },
] as const

export function DemoWipeMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("dwm_usun_01")
  const [kind, setKind] = useState("usun")
  const [ref, setRef] = useState("fixture://demo-wipe-mark/")
  const save = useMutation({
    mutationFn: () =>
      createDemoWipeMark(makeDemoWipeMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("dwm_usun_01")
      setKind("usun")
      setRef("fixture://demo-wipe-mark/")
      void qc.invalidateQueries({
        queryKey: ["demo-wipe-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-dwm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code demo wipe"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        wipe_kind
        <select
          aria-label="wipe_kind usun retain other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {WIPE_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref demo wipe"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik wipe demo
      </Button>
    </form>
  )
}
