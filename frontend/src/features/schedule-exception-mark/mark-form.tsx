import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildScheduleExceptionMarkWrite,
  saveScheduleExceptionMark,
} from "@/lib/schedule-exception-marks-api"

const KINDS = [
  { value: "delay", label: "delay" },
  { value: "cancel", label: "cancel" },
  { value: "reroute", label: "reroute" },
  { value: "other", label: "other" },
] as const

export function ScheduleExceptionMarkEditor(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("delay_01")
  const [kind, setKind] = useState("delay")
  const [origin, setOrigin] = useState("fixture://schedule-exception-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveScheduleExceptionMark(
        buildScheduleExceptionMarkWrite({ code, kind, origin }),
      ),
    onSuccess: () => {
      setCode("delay_01")
      setKind("delay")
      setOrigin("fixture://schedule-exception-mark/")
      void qc.invalidateQueries({ queryKey: ["schedule-exception-marks", props.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-schedule-exception-mark="editor"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Wyjątek harmonogramu jako etykieta HITL. Bez silnika schedule i bez ETA.
      </p>
      <label className="grid gap-1 text-xs">
        Kod
        <input
          aria-label="Kod znacznika schedule exception"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        exception_kind
        <select
          aria-label="Rodzaj schedule exception"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {KINDS.map((row) => (
            <option key={row.value} value={row.value}>
              {row.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="Pochodzenie schedule exception"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit">
        Zapisz schedule exception
      </Button>
    </form>
  )
}
