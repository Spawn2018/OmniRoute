import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchTenancyUsers, gdprSubjects } from "@/lib/api"
import {
  fetchGdprRequests,
  fulfillGdprRequest,
  recordGdprRequest,
} from "@/lib/gdpr-requests-api"
import { getTenantContext } from "@/lib/tenant"

type RequestDraft = {
  userId: string
  kind: "access" | "erasure"
  sourceRef: string
}

const FRESH: RequestDraft = {
  userId: "",
  kind: "access",
  sourceRef: "fixture://gdpr-request/",
}

function RequestSaveStrip(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(FRESH)
  const save = useMutation({
    mutationFn: () =>
      recordGdprRequest({
        app_user_id: draft.userId.trim(),
        request_kind: draft.kind,
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...FRESH })
      void client.invalidateQueries({ queryKey: ["gdpr-requests", args.organizationId] })
    },
  })
  return (
    <form
      className="flex flex-col gap-2"
      data-gdpr="request-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <label className="text-xs" htmlFor="app_user_id">
        Konto
        <Input
          id="app_user_id"
          name="app_user_id"
          placeholder="app_user_id"
          value={draft.userId}
          onChange={(event) => setDraft({ ...draft, userId: event.target.value })}
          required
        />
      </label>
      <label className="text-xs" htmlFor="request_kind">
        Rodzaj
        <select
          id="request_kind"
          name="request_kind"
          className="border-input bg-background h-8 w-full rounded-md border px-2 text-xs"
          value={draft.kind}
          onChange={(event) =>
            setDraft({ ...draft, kind: event.target.value === "erasure" ? "erasure" : "access" })
          }
        >
          <option value="access">access</option>
          <option value="erasure">erasure</option>
        </select>
      </label>
      <label className="text-xs" htmlFor="source_ref">
        Źródło
        <Input
          id="source_ref"
          name="source_ref"
          placeholder="source_ref"
          value={draft.sourceRef}
          onChange={(event) => setDraft({ ...draft, sourceRef: event.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz wniosek
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

function RequestRows(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const rows = useQuery({
    queryKey: ["gdpr-requests", args.organizationId],
    queryFn: fetchGdprRequests,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const fulfill = useMutation({
    mutationFn: fulfillGdprRequest,
    onSuccess: () => {
      void client.invalidateQueries({ queryKey: ["gdpr-requests", args.organizationId] })
      void client.invalidateQueries({ queryKey: ["gdpr-users", args.organizationId] })
    },
  })
  return (
    <>
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      {fulfill.isError ? <CatalogError error={fulfill.error} /> : null}
      <ul data-gdpr="requests">
        {(rows.data ?? []).map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.request_kind} {row.status} {row.app_user_id} {row.source_ref}{" "}
            {row.status === "open" ? (
              <Button
                type="button"
                disabled={fulfill.isPending}
                onClick={() => fulfill.mutate(row.id)}
              >
                Wypełnij
              </Button>
            ) : null}
          </li>
        ))}
      </ul>
    </>
  )
}

export function GdprPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const users = useQuery({
    queryKey: ["gdpr-users", ctx.organizationId],
    queryFn: fetchTenancyUsers,
    enabled: ready,
    retry: false,
  })
  const inventory = gdprSubjects(users.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-gdpr="board">
      <CatalogHeading
        title="RODO"
        subtitle="gdpr M-56 · wniosek access/erasure · tombstone konta · nie DPIA"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {users.isError ? <CatalogError error={users.error} /> : null}
      <ul>
        {inventory.map((row) => (
          <li key={row.id} className="text-xs">
            {row.email} {row.display_name}{" "}
            <Link className="underline" to="/tenancy/users">
              konto
            </Link>
          </li>
        ))}
      </ul>
      {ready ? <RequestSaveStrip organizationId={ctx.organizationId} /> : null}
      {ready ? <RequestRows organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
