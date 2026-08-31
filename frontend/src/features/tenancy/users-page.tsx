import { Link } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { fetchTenancyUsers, getTenantContext, type AppUser } from "@/lib/api"

const columnHelper = createColumnHelper<AppUser>()

const columns = [
  columnHelper.accessor("email", {
    id: "email",
    header: "Email",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("display_name", {
    id: "display_name",
    header: "Nazwa",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("id", {
    id: "id",
    header: "ID",
    cell: (info) => (
      <span className="font-mono text-xs text-muted-foreground">{info.getValue()}</span>
    ),
  }),
]

const COLUMN_LABELS = {
  email: "Email",
  display_name: "Nazwa",
  id: "ID",
}

export function UsersPage() {
  const ctx = getTenantContext()
  const query = useQuery({
    queryKey: ["tenancy", "users", ctx.organizationId],
    queryFn: fetchTenancyUsers,
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  return (
    <div className="space-y-3">
      <div>
        <h2 className="text-base font-semibold">Użytkownicy tenanta</h2>
        <p className="text-xs text-muted-foreground">
          DataTableShell · widoki RLS · ColumnEditor (checkbox + DnD)
        </p>
      </div>

      {!ctx.organizationId || !ctx.userId ? (
        <div className="rounded-md border border-border bg-card p-3 text-sm">
          Ustaw identyfikatory sesji na stronie{" "}
          <Link className="underline" to="/session">
            Sesja
          </Link>
          .
        </div>
      ) : null}

      {query.isLoading ? <div className="text-sm text-muted-foreground">Ładowanie…</div> : null}

      {query.isError ? (
        <div className="rounded-md border border-destructive/40 bg-card p-3 text-sm text-destructive">
          {(query.error as Error).message}
        </div>
      ) : null}

      {query.data ? (
        <DataTableShell
          tableKey="tenancy.users"
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj użytkownika…"
        />
      ) : null}
    </div>
  )
}
