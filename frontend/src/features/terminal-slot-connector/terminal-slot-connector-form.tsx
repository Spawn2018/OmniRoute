import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { persistTerminalSlotConnector, toSlotWrite } from "@/lib/terminal-slot-connectors-api"

type SlotDraft = {
  slotKey: string
  gateToken: string
  regime: string
  openStamp: string
  closeStamp: string
  cutStamp: string
  originHint: string
}

const EMPTY_SLOT: SlotDraft = {
  slotKey: "gdynia_bct",
  gateToken: "plgdy_bct",
  regime: "email_hitl",
  openStamp: "06:00",
  closeStamp: "22:00",
  cutStamp: "16:00",
  originHint: "fixture://terminal-slot-connector/",
}

const REGIMES = ["api", "email_hitl", "portal_task", "unsupported"] as const

function SlotIdentityFields(args: { draft: SlotDraft; onDraft: (next: SlotDraft) => void }) {
  const { draft, onDraft } = args
  return (
    <>
      <label className="flex flex-col gap-1 text-xs">
        Kod konektora (snake 2–32)
        <input
          aria-label="Kod konektora slotu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => onDraft({ ...draft, slotKey: change.target.value })}
          required
          value={draft.slotKey}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod terminalu (dana, nie FK)
        <input
          aria-label="Kod terminalu slotu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => onDraft({ ...draft, gateToken: change.target.value })}
          required
          value={draft.gateToken}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Tryb capability
        <select
          aria-label="Tryb konektora slotu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => onDraft({ ...draft, regime: change.target.value })}
          value={draft.regime}
        >
          {REGIMES.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
    </>
  )
}

function GateHoursFields(args: { draft: SlotDraft; onDraft: (next: SlotDraft) => void }) {
  const { draft, onDraft } = args
  return (
    <fieldset className="grid gap-3 rounded-md border p-3">
      <legend className="px-1 text-xs">Godziny N4 (lokalne, nie countdown)</legend>
      <label className="flex flex-col gap-1 text-xs">
        Otwarcie
        <input
          aria-label="Godzina otwarcia terminalu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => onDraft({ ...draft, openStamp: change.target.value })}
          required
          type="time"
          value={draft.openStamp}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Zamknięcie
        <input
          aria-label="Godzina zamknięcia terminalu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => onDraft({ ...draft, closeStamp: change.target.value })}
          required
          type="time"
          value={draft.closeStamp}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Odcięcie
        <input
          aria-label="Godzina odcięcia terminalu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => onDraft({ ...draft, cutStamp: change.target.value })}
          required
          type="time"
          value={draft.cutStamp}
        />
      </label>
    </fieldset>
  )
}

export function TerminalSlotSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SLOT)
  const persist = useMutation({
    mutationFn: () => persistTerminalSlotConnector(toSlotWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_SLOT })
      void cache.invalidateQueries({ queryKey: ["terminal-slot-connectors", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-terminal-slot-connector="terminal-slot-connector-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Capability slotu i godziny bramy to dane operatora. Serwis nie woła Navis N4
        ani portalu. Potwierdzenia z adaptera API tu nie zapiszesz.
      </p>
      <SlotIdentityFields draft={draft} onDraft={setDraft} />
      <GateHoursFields draft={draft} onDraft={setDraft} />
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://terminal-slot-connector/…)"
        ariaLabel="Pochodzenie konektora slotu"
        value={draft.originHint}
        onChange={(originHint) => setDraft({ ...draft, originHint })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz konektor slotu
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
