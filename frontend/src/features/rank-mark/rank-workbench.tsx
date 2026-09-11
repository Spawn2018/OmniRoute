import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listRankMarks, persistRankMark, rankWrite } from "@/lib/rank-marks-api"

type AxisDraft = {
  axis: string
  origin: string
}

const BLANK_AXIS: AxisDraft = {
  axis: "price",
  origin: "fixture://rank-mark/",
}

const AXES = ["price", "transit", "reliability", "carbon", "other"] as const

function RankComposer(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(BLANK_AXIS)
  const persist = useMutation({
    mutationFn: () => persistRankMark(rankWrite(draft)),
    onSuccess: () => {
      setDraft({ ...BLANK_AXIS })
      void cache.invalidateQueries({ queryKey: ["purchase-axis-stamps", args.organizationId] })
    },
  })
  return (
    <form
      className="border p-3 rounded-md space-y-3"
      data-rank-mark="kind-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId && persist.isPending === false) persist.mutate()
      }}
    >
      <p className="text-muted-foreground text-xs">
        Pięć osi zakupu. To nie jest auto-award i nie paczka szkiców z Top N.
        Marża zostaje na `/charges`.
      </p>
      <fieldset className="overflow-x-auto">
        <legend className="text-xs mb-1">Oś rankingu (allowlista)</legend>
        <div className="flex gap-3 whitespace-nowrap">
          {AXES.map((axis) => (
            <label key={axis} className="text-xs font-mono inline-flex gap-1 items-center">
              <input
                type="radio"
                name="purchase-axis"
                aria-label={`Oś ${axis}`}
                checked={draft.axis === axis}
                onChange={() => setDraft({ ...draft, axis })}
                value={axis}
              />
              {axis}
            </label>
          ))}
        </div>
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://rank-mark/…)"
        ariaLabel="source_ref osi rankingu"
        value={draft.origin}
        onChange={(origin) => setDraft({ ...draft, origin })}
      />
      <Button type="submit" disabled={args.organizationId === null || persist.isPending}>
        Zapisz oś rankingu
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function RankMenu(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["purchase-axis-stamps", args.organizationId],
    queryFn: listRankMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const rows = listed.data ?? []
  return (
    <div>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <menu data-rank-mark="rows" className="m-0 list-none p-0 text-xs font-mono">
        {rows.map((row) => (
          <li key={row.id} data-rank-kind={row.rank_kind} className="py-0.5">
            {row.rank_kind} — {row.source_ref}
          </li>
        ))}
      </menu>
    </div>
  )
}

export function RankWorkbench(args: { organizationId: string | null }) {
  return (
    <div className="flex flex-col gap-6 xl:flex-row xl:items-start">
      <RankComposer organizationId={args.organizationId} />
      <RankMenu organizationId={args.organizationId} />
    </div>
  )
}
