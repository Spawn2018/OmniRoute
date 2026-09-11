import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useId, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildTimeToFixMarkWrite, saveTimeToFixMark } from "@/lib/time-to-fix-marks-api"

const FIX_OPTIONS: ReadonlyArray<{ id: string; caption: string }> = [
  { id: "open", caption: "otwarty" },
  { id: "wip", caption: "w toku" },
  { id: "done", caption: "zamknięty" },
  { id: "other", caption: "inny" },
]

export function TimeToFixMarkEditor(props: { organizationId: string | null }) {
  const formId = useId()
  const qc = useQueryClient()
  const [markCode, setMarkCode] = useState("open_01")
  const [fixKind, setFixKind] = useState("open")
  const [sourceRef, setSourceRef] = useState("fixture://time-to-fix-mark/")
  const mutation = useMutation({
    mutationFn: async () =>
      saveTimeToFixMark(
        buildTimeToFixMarkWrite({ code: markCode, kind: fixKind, origin: sourceRef }),
      ),
    onSuccess: () => {
      setMarkCode("open_01")
      setFixKind("open")
      setSourceRef("fixture://time-to-fix-mark/")
      void qc.invalidateQueries({ queryKey: ["time-to-fix-marks", props.organizationId] })
    },
  })

  function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (!props.organizationId) return
    mutation.mutate()
  }

  return (
    <form id={formId} className="max-w-md space-y-3" data-ttf="write" onSubmit={onSubmit}>
      <p className="text-xs text-muted-foreground">
        Status naprawy (TIME-TO-FIX) zapisany ręcznie. Brak automatycznego SLA SQL.
      </p>
      <div className="grid gap-1 text-xs">
        <span>Kod znacznika</span>
        <input
          aria-label="Kod znacznika TIME-TO-FIX"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(event) => setMarkCode(event.target.value)}
          required
          value={markCode}
        />
      </div>
      <div className="grid gap-1 text-xs">
        <span>Stan (`fix_kind`)</span>
        <select
          aria-label="Rodzaj TIME-TO-FIX"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(event) => setFixKind(event.target.value)}
          value={fixKind}
        >
          {FIX_OPTIONS.map((option) => (
            <option key={option.id} value={option.id}>
              {option.id} — {option.caption}
            </option>
          ))}
        </select>
      </div>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="Pochodzenie TIME-TO-FIX"
        value={sourceRef}
        onChange={setSourceRef}
      />
      {mutation.error ? <CatalogError error={mutation.error} /> : null}
      <Button disabled={!props.organizationId || mutation.isPending} type="submit">
        Zapisz TIME-TO-FIX
      </Button>
    </form>
  )
}
