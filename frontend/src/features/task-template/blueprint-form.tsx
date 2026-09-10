import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  blueprintWrite,
  listTaskTemplates,
  persistTaskTemplate,
} from "@/lib/task-templates-api"

type BlueprintDraft = {
  codeToken: string
  whenNote: string
  originStamp: string
}

const EMPTY_BLUEPRINT: BlueprintDraft = {
  codeToken: "gate_in",
  whenNote: "container at CY",
  originStamp: "fixture://task-template/",
}

function BlueprintField(args: {
  label: string
  aria: string
  value: string
  placeholder?: string
  onValue: (next: string) => void
}) {
  return (
    <label className="flex flex-col gap-1 text-xs">
      {args.label}
      <input
        aria-label={args.aria}
        className="h-9 rounded-md border bg-background px-2 font-mono"
        value={args.value}
        placeholder={args.placeholder}
        onChange={(change) => args.onValue(change.target.value)}
        required
      />
    </label>
  )
}

function BlueprintFields(args: {
  draft: BlueprintDraft
  onDraft: (next: BlueprintDraft) => void
}) {
  const draft = args.draft
  return (
    <>
      <p className="text-muted-foreground text-xs">
        Kod szablonu i warunek to dane. Serwis nie ewaluuje `applies_when`, nie stawia zadania na
        zleceniu i nie woła outboxa. Marża zostaje na `/charges`.
      </p>
      <BlueprintField
        label="Kod szablonu (snake)"
        aria="Kod szablonu zadania"
        value={draft.codeToken}
        onValue={(codeToken) => args.onDraft({ ...draft, codeToken })}
      />
      <BlueprintField
        label="Warunek (applies_when)"
        aria="Warunek szablonu zadania"
        value={draft.whenNote}
        onValue={(whenNote) => args.onDraft({ ...draft, whenNote })}
      />
      <BlueprintField
        label="Pochodzenie zapisu"
        aria="source_ref szablonu zadania"
        value={draft.originStamp}
        placeholder="tenant:manual albo fixture://task-template/…"
        onValue={(originStamp) => args.onDraft({ ...draft, originStamp })}
      />
    </>
  )
}

function BlueprintSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_BLUEPRINT)
  const persist = useMutation({
    mutationFn: () => persistTaskTemplate(blueprintWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_BLUEPRINT })
      void cache.invalidateQueries({ queryKey: ["task-blueprints", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3"
      data-task-template="blueprint-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId !== null && persist.isPending === false) {
          persist.mutate()
        }
      }}
    >
      <BlueprintFields draft={draft} onDraft={setDraft} />
      <Button type="submit" disabled={args.organizationId === null || persist.isPending}>
        Zapisz szablon zadania
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function BlueprintRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["task-blueprints", args.organizationId],
    queryFn: listTaskTemplates,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <div>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-task-template="rows" className="flex list-none flex-col gap-1 p-0 text-xs font-mono">
        {(listed.data ?? []).map((row) => (
          <li key={row.id}>
            {row.template_code} · {row.applies_when}
          </li>
        ))}
      </ul>
    </div>
  )
}

export function BlueprintPanel(args: { organizationId: string | null }) {
  return (
    <div className="flex flex-col gap-8 md:flex-row md:items-start">
      <BlueprintSave organizationId={args.organizationId} />
      <BlueprintRows organizationId={args.organizationId} />
    </div>
  )
}
