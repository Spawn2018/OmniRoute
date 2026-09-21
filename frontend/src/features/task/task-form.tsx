import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listTasks, persistTask, taskWrite } from "@/lib/tasks-api"

type TaskDraft = {
  codeToken: string
  templateToken: string
  statusToken: string
  originStamp: string
}

const EMPTY_TASK: TaskDraft = {
  codeToken: "gate_check_01",
  templateToken: "gate_in",
  statusToken: "open",
  originStamp: "fixture://task/",
}

function TaskField(args: {
  label: string
  aria: string
  value: string
  onValue: (next: string) => void
}) {
  return (
    <label className="flex flex-col gap-1 text-xs">
      {args.label}
      <input
        aria-label={args.aria}
        className="h-9 rounded-md border bg-background px-2 font-mono"
        value={args.value}
        onChange={(change) => args.onValue(change.target.value)}
        required
      />
    </label>
  )
}

function TaskFields(args: {
  draft: TaskDraft
  onDraft: (next: TaskDraft) => void
}) {
  const draft = args.draft
  return (
    <>
      <p className="text-muted-foreground text-xs">
        Wpis zadania z kodem szablonu jako tekstem. Matching SQL, FK zlecenia i
        outbox zostaja poza tym katalogiem. Marza zostaje na `/charges`.
      </p>
      <TaskField
        label="Kod zadania (snake)"
        aria="Kod zadania"
        value={draft.codeToken}
        onValue={(codeToken) => args.onDraft({ ...draft, codeToken })}
      />
      <TaskField
        label="Kod szablonu (snake)"
        aria="Kod szablonu zadania"
        value={draft.templateToken}
        onValue={(templateToken) => args.onDraft({ ...draft, templateToken })}
      />
      <TaskField
        label="Status (open|done|skipped|other)"
        aria="Status zadania"
        value={draft.statusToken}
        onValue={(statusToken) => args.onDraft({ ...draft, statusToken })}
      />
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://task/…)"
        ariaLabel="source_ref zadania"
        value={draft.originStamp}
        onChange={(originStamp) => args.onDraft({ ...draft, originStamp })}
      />
    </>
  )
}

function TaskSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_TASK)
  const persist = useMutation({
    mutationFn: () => persistTask(taskWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_TASK })
      void cache.invalidateQueries({ queryKey: ["tasks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3"
      data-task="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId !== null && persist.isPending === false) {
          persist.mutate()
        }
      }}
    >
      <TaskFields draft={draft} onDraft={setDraft} />
      <Button type="submit" disabled={args.organizationId === null || persist.isPending}>
        Zapisz zadanie
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function TaskRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["tasks", args.organizationId],
    queryFn: listTasks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <div>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-task="rows" className="flex list-none flex-col gap-1 p-0 text-xs font-mono">
        {(listed.data ?? []).map((row) => (
          <li key={row.id}>
            {row.task_code} · {row.template_code} · {row.status_kind}
          </li>
        ))}
      </ul>
    </div>
  )
}

export function TaskPanel(args: { organizationId: string | null }) {
  return (
    <div className="flex flex-col gap-8 md:flex-row md:items-start">
      <TaskSave organizationId={args.organizationId} />
      <TaskRows organizationId={args.organizationId} />
    </div>
  )
}
