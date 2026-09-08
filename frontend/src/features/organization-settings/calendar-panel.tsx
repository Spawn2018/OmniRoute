import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  calendarDayWrite,
  fetchCalendarDays,
  fetchWorkingDay,
  saveCalendarDay,
} from "@/lib/organization-calendar-api"
import { getTenantContext } from "@/lib/tenant"

export function CalendarOverridePanel(args: { canWrite: boolean }) {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [country, setCountry] = useState("PL")
  const [day, setDay] = useState("2026-09-04")
  const [kind, setKind] = useState("holiday")
  const [probe, setProbe] = useState<boolean | null>(null)
  const listQuery = useQuery({
    queryKey: ["organization-calendars", ctx.organizationId, country],
    queryFn: () => fetchCalendarDays(country),
    enabled: args.canWrite,
    retry: false,
  })
  const save = useMutation({
    mutationFn: () => saveCalendarDay(calendarDayWrite({ country, day, kind })),
    onSuccess: () => {
      setProbe(null)
      void queryClient.invalidateQueries({
        queryKey: ["organization-calendars", ctx.organizationId, country],
      })
    },
  })
  const check = useMutation({
    mutationFn: () => fetchWorkingDay({ country, day }),
    onSuccess: (body) => {
      setProbe(body.is_working_day)
    },
  })
  const rows = listQuery.data ?? []
  return (
    <aside className="space-y-2 rounded-md border border-border bg-card p-3" data-organization-calendar="days">
      <p className="text-sm font-medium">Kalendarz dni roboczych</p>
      <p className="text-xs text-muted-foreground">
        Święto albo jawny dzień roboczy per kraj. is_working_day liczy SQL, nie +3 kalendarzowe.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod kraju ISO
        <Input
          aria-label="Kod kraju ISO kalendarza"
          maxLength={2}
          value={country}
          onChange={(event) => setCountry(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Dzień
        <input
          aria-label="Dzień kalendarza"
          className="h-8 rounded-md border border-border bg-card px-2 text-sm"
          type="date"
          value={day}
          onChange={(event) => setDay(event.target.value)}
        />
      </label>
      <fieldset className="space-y-1 text-xs">
        <legend>Rodzaj dnia</legend>
        <label className="inline-flex items-center gap-1">
          <input
            checked={kind === "holiday"}
            name="calendar-day-kind"
            type="radio"
            value="holiday"
            onChange={() => setKind("holiday")}
          />
          święto
        </label>
        <label className="ml-3 inline-flex items-center gap-1">
          <input
            checked={kind === "working"}
            name="calendar-day-kind"
            type="radio"
            value="working"
            onChange={() => setKind("working")}
          />
          dzień roboczy
        </label>
      </fieldset>
      <div className="flex flex-wrap gap-2">
        <Button
          type="button"
          disabled={!args.canWrite || save.isPending}
          onClick={() => save.mutate()}
        >
          Zapisz dzień
        </Button>
        <Button
          type="button"
          disabled={!args.canWrite || check.isPending}
          onClick={() => check.mutate()}
        >
          Sprawdź dzień roboczy
        </Button>
      </div>
      {save.isError ? <p className="text-sm text-destructive">{(save.error as Error).message}</p> : null}
      {check.isError ? <p className="text-sm text-destructive">{(check.error as Error).message}</p> : null}
      {probe === null ? null : (
        <p className="text-sm">{probe ? "dzień roboczy" : "dzień wolny"}</p>
      )}
      <ul className="space-y-1">
        {rows.map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.calendar_day} {row.day_kind}
          </li>
        ))}
      </ul>
    </aside>
  )
}
