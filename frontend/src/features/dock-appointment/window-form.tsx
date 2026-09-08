import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { dockWrite, persistDock, listDocks } from "@/lib/dock-appointments-api"

type WindowDraft = {
  orderKey: string
  haltRef: string
  slotToken: string
  stageMark: string
  dayMark: string
  openMark: string
  closeMark: string
  originNote: string
}

const EMPTY_WINDOW: WindowDraft = {
  orderKey: "",
  haltRef: "",
  slotToken: "",
  stageMark: "advised",
  dayMark: "2026-09-09",
  openMark: "08:00",
  closeMark: "10:00",
  originNote: "fixture://dock-appointment/",
}

function ClockField(args: {
  spoken: string
  kind: "text" | "date" | "time"
  filled: string
  put: (next: string) => void
}) {
  return (
    <label className="flex flex-col gap-1 text-xs">
      {args.spoken}
      <input
        type={args.kind}
        aria-label={args.spoken}
        className="h-9 rounded-md border bg-background px-2 font-mono"
        value={args.filled}
        onChange={(change) => args.put(change.target.value)}
        required
      />
    </label>
  )
}

function WindowFields(args: { draft: WindowDraft; put: (next: WindowDraft) => void }) {
  const row = args.draft
  return (
    <div className="flex max-w-md flex-col gap-2">
      <ClockField
        spoken="Identyfikator zlecenia awizacji"
        kind="text"
        filled={row.orderKey}
        put={(orderKey) => args.put({ ...row, orderKey })}
      />
      <ClockField
        spoken="Identyfikator stopu awizacji"
        kind="text"
        filled={row.haltRef}
        put={(haltRef) => args.put({ ...row, haltRef })}
      />
      <ClockField
        spoken="Kod snake awizacji"
        kind="text"
        filled={row.slotToken}
        put={(slotToken) => args.put({ ...row, slotToken })}
      />
      <ClockField
        spoken="Status awizacji doku"
        kind="text"
        filled={row.stageMark}
        put={(stageMark) => args.put({ ...row, stageMark })}
      />
      <ClockField
        spoken="Dzień okna doku"
        kind="date"
        filled={row.dayMark}
        put={(dayMark) => args.put({ ...row, dayMark })}
      />
      <ClockField
        spoken="Początek okna lokalnego"
        kind="time"
        filled={row.openMark}
        put={(openMark) => args.put({ ...row, openMark })}
      />
      <ClockField
        spoken="Koniec okna lokalnego"
        kind="time"
        filled={row.closeMark}
        put={(closeMark) => args.put({ ...row, closeMark })}
      />
      <ClockField
        spoken="Pochodzenie zapisu awizacji"
        kind="text"
        filled={row.originNote}
        put={(originNote) => args.put({ ...row, originNote })}
      />
    </div>
  )
}

function WindowSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_WINDOW)
  const persist = useMutation({
    mutationFn: () => persistDock(dockWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_WINDOW })
      void cache.invalidateQueries({ queryKey: ["docks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex flex-col gap-3"
      data-dock="window-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="max-w-md text-xs text-muted-foreground">
        Okno TIME na stop magazynu (strefa albo adres). Port UN/LOCODE odpada — to T8, nie
        cross-dock. Koniec musi być po starcie. Nie WMS.
      </p>
      <WindowFields draft={draft} put={setDraft} />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz awizację doku
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function DockRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["docks", args.organizationId],
    queryFn: listDocks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-dock="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap gap-2 font-mono">
            <span>{row.appointment_code}</span>
            <span>{row.appointment_status}</span>
            <span>
              {row.window_date} {row.window_start_local}–{row.window_end_local}
            </span>
            <Link className="underline" to="/shipments">
              zlecenie
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function DockWindowForm(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <WindowSave organizationId={args.organizationId} />
      <DockRows organizationId={args.organizationId} />
    </>
  )
}
