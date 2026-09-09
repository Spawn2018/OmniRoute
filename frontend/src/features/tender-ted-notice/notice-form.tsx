import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listTedMarks, persistTedMark, tedWrite } from "@/lib/tender-ted-notices-api"

type TedDraft = {
  boardStamp: string
  noticeStamp: string
  originStamp: string
}

const EMPTY_TED: TedDraft = {
  boardStamp: "",
  noticeStamp: "123456-2024",
  originStamp: "fixture://tender-ted-notice/",
}

function TedSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_TED)
  const persist = useMutation({
    mutationFn: () => persistTedMark(tedWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_TED })
      void cache.invalidateQueries({ queryKey: ["ted-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-ted-notice="notice-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Numer ogłoszenia TED przy nagłówku. CO₂ zostaje leftover. Status nagłówka nie zmienia się tu.
        Marża zostaje na `/charges`. Nie ma tu fetcha do TED.europa.eu.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu ogłoszenia TED"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Numer ogłoszenia TED
        <input
          aria-label="Numer ogłoszenia TED"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.noticeStamp}
          onChange={(change) => setDraft({ ...draft, noticeStamp: change.target.value })}
          required
        />
      </label>
      <p className="text-xs text-muted-foreground">source_ref: tenant:manual albo fixture://tender-ted-notice/…</p>
      <input
        aria-label="source_ref ogłoszenia TED"
        className="h-9 max-w-lg rounded-md border bg-background px-2 font-mono text-xs"
        value={draft.originStamp}
        onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
        required
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz ogłoszenie TED
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function TedRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["ted-marks", args.organizationId],
    queryFn: listTedMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-ted-notice="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.notice_number}
          </li>
        ))}
      </ul>
    </>
  )
}

export function TedPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <TedSave organizationId={args.organizationId} />
      <TedRows organizationId={args.organizationId} />
    </div>
  )
}
