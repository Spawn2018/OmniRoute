import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildLclConsoleMarkWrite, saveLclConsoleMark } from "@/lib/lcl-console-marks-api"

const CONSOLE_KINDS = ["console", "cfs", "other"] as const

export function LclConsoleMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("lcm_console_01")
  const [kind, setKind] = useState<string>("console")
  const [origin, setOrigin] = useState("fixture://lcl-console-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveLclConsoleMark(buildLclConsoleMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("lcm_console_01")
      setKind("console")
      setOrigin("fixture://lcl-console-mark/")
      void cache.invalidateQueries({
        queryKey: ["lcl-console-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-lcl-console-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance konsoli LCL/CFS jako katalog HITL. Live CFS i kalkulacja CBM nie wchodzą do tego
        wiersza.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod stance konsoli LCL"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Rodzaj konsoli
        <select
          aria-label="Rodzaj stance konsoli LCL"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(event) => setKind(event.target.value)}
          value={kind}
        >
          {CONSOLE_KINDS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://lcl-console-mark/…)"
        ariaLabel="Pochodzenie stance konsoli LCL"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stance konsoli LCL
      </Button>
    </form>
  )
}
