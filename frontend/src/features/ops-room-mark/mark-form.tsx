import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildOpsRoomMarkWrite, saveOpsRoomMark } from "@/lib/ops-room-marks-api"

const LAYER_KINDS = [
  { value: "shift", label: "Zmiana (shift)" },
  { value: "board", label: "Tablica (board)" },
  { value: "escalation", label: "Eskalacja" },
  { value: "other", label: "Inne" },
] as const

export function OpsRoomMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("ops_shift_01")
  const [kind, setKind] = useState("shift")
  const [origin, setOrigin] = useState("fixture://ops-room-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveOpsRoomMark(buildOpsRoomMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("ops_shift_01")
      setKind("shift")
      setOrigin("fixture://ops-room-mark/")
      void cache.invalidateQueries({
        queryKey: ["ops-room-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3 rounded-md border border-slate-600/25 bg-slate-50/30 p-3 dark:bg-slate-950/20"
      data-ops-room-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Warstwa działająca sali operacyjnej jako katalog HITL. Koalescencja N8 i
        widok sklejony nie wchodzą do tego wiersza.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod warstwy sali operacyjnej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Rodzaj warstwy
        <select
          aria-label="Rodzaj warstwy shift board escalation other"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          {LAYER_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://ops-room-mark/…)"
        ariaLabel="Pochodzenie warstwy sali operacyjnej"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz warstwę sali
      </Button>
    </form>
  )
}
