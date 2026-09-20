import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { groupWrite, listStopGroups, persistStopGroup } from "@/lib/stop-groups-api"

type GroupDraft = {
  shipmentToken: string
  groupCode: string
  originStamp: string
}

const EMPTY_GROUP: GroupDraft = {
  shipmentToken: "",
  groupCode: "",
  originStamp: "fixture://stop-group/",
}

function DraftField(args: {
  label: string
  value: string
  onValue: (next: string) => void
}) {
  return (
    <label className="grid gap-1 text-xs">
      <span>{args.label}</span>
      <input
        aria-label={args.label}
        className="h-9 rounded-md border bg-background px-2 font-mono"
        value={args.value}
        onChange={(change) => args.onValue(change.target.value)}
        required
      />
    </label>
  )
}

function GroupDraftFields(args: {
  draft: GroupDraft
  put: (next: GroupDraft) => void
}) {
  return (
    <>
      <DraftField
        label="Identyfikator zlecenia"
        value={args.draft.shipmentToken}
        onValue={(shipmentToken) => args.put({ ...args.draft, shipmentToken })}
      />
      <DraftField
        label="Kod grupy"
        value={args.draft.groupCode}
        onValue={(groupCode) => args.put({ ...args.draft, groupCode })}
      />
      <DraftField
        label="Pochodzenie zapisu grupy"
        value={args.draft.originStamp}
        onValue={(originStamp) => args.put({ ...args.draft, originStamp })}
      />
    </>
  )
}

function GroupSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_GROUP)
  const persist = useMutation({
    mutationFn: () => persistStopGroup(groupWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_GROUP })
      void cache.invalidateQueries({ queryKey: ["stop-groups", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-stop-group="group-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Nagłówek grupy punktów na zleceniu. Kilka grup na jedno zlecenie jest
        dozwolone. Kod na punkcie (`stop_group_code`) zostaje osobno — to nie
        członkostwo.
      </p>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
      <GroupDraftFields draft={draft} put={setDraft} />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz grupę punktów
      </Button>
    </form>
  )
}

function StopGroupMarks(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["stop-groups", args.organizationId],
    queryFn: listStopGroups,
    enabled: args.organizationId !== null,
    retry: false,
  })
  const marks = listed.data ?? []
  return (
    <div data-stop-group="rows" className="flex flex-col gap-1 text-xs">
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      {marks.map((row) => (
        <p key={row.id} className="flex flex-wrap gap-2 font-mono">
          <span>{row.group_code}</span>
          <Link className="underline" to="/shipments">
            zlecenie
          </Link>
        </p>
      ))}
    </div>
  )
}

export function StopGroupPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <div className="flex flex-col gap-4">
      <GroupSave organizationId={args.organizationId} />
      <StopGroupMarks organizationId={args.organizationId} />
    </div>
  )
}
