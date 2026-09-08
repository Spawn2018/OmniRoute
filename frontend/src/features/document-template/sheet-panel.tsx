import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listSheetMarks, persistSheetMark, sheetWrite } from "@/lib/document-templates-api"

const KINDS = ["own_label", "cmr"] as const
const TONGUES = ["pl", "en"] as const
const EXITS = ["html_print"] as const

type SheetDraft = {
  kindToken: string
  tongueToken: string
  layoutToken: string
  exitToken: string
  originStamp: string
}

const EMPTY_SHEET: SheetDraft = {
  kindToken: "own_label",
  tongueToken: "pl",
  layoutToken: "own-label-pl",
  exitToken: "html_print",
  originStamp: "fixture://document-template/",
}

function SheetSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SHEET)
  const persist = useMutation({
    mutationFn: () => persistSheetMark(sheetWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_SHEET })
      void cache.invalidateQueries({ queryKey: ["sheet-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-document-template="sheet-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Szablon wydruku jako wskazanie layoutu. To nie PDF, nie etykieta sieci i nie
        `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj szablonu
        <select
          aria-label="Rodzaj szablonu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindToken}
          onChange={(change) => setDraft({ ...draft, kindToken: change.target.value })}
        >
          {KINDS.map((kind) => (
            <option key={kind} value={kind}>
              {kind}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Język layoutu
        <select
          aria-label="Język layoutu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.tongueToken}
          onChange={(change) => setDraft({ ...draft, tongueToken: change.target.value })}
        >
          {TONGUES.map((tongue) => (
            <option key={tongue} value={tongue}>
              {tongue}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Wskazanie layoutu
        <input
          aria-label="Wskazanie layoutu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.layoutToken}
          onChange={(change) => setDraft({ ...draft, layoutToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj wyjścia
        <select
          aria-label="Rodzaj wyjścia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.exitToken}
          onChange={(change) => setDraft({ ...draft, exitToken: change.target.value })}
        >
          {EXITS.map((exit) => (
            <option key={exit} value={exit}>
              {exit}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu szablonu
        <input
          aria-label="Pochodzenie zapisu szablonu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz szablon wydruku
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function SheetRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["sheet-marks", args.organizationId],
    queryFn: listSheetMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-document-template="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap gap-2 font-mono">
            <span>{row.template_kind}</span>
            <span>{row.language}</span>
            <span>{row.layout_ref}</span>
            <span>{row.output_kind}</span>
          </li>
        ))}
      </ul>
    </>
  )
}

export function SheetKindPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <SheetSave organizationId={args.organizationId} />
      <SheetRows organizationId={args.organizationId} />
    </>
  )
}
