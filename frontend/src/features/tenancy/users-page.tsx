import { Link } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { fetchTenancyUsers, getTenantContext } from "@/lib/api"

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
          Lista read-only przez API · ColumnEditor w plasterze 0.6
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

      {query.isLoading ? (
        <div className="text-sm text-muted-foreground">Ładowanie…</div>
      ) : null}

      {query.isError ? (
        <div className="rounded-md border border-destructive/40 bg-card p-3 text-sm text-destructive">
          {(query.error as Error).message}
        </div>
      ) : null}

      {query.data ? (
        <div className="overflow-auto rounded-md border border-border bg-card">
          <table className="w-full min-w-[480px] border-collapse text-sm">
            <thead className="sticky top-0 bg-muted">
              <tr className="border-b border-border text-left text-xs text-muted-foreground">
                <th className="px-3 py-1.5 font-medium">Email</th>
                <th className="px-3 py-1.5 font-medium">Nazwa</th>
                <th className="px-3 py-1.5 font-medium">ID</th>
              </tr>
            </thead>
            <tbody>
              {query.data.length === 0 ? (
                <tr>
                  <td colSpan={3} className="px-3 py-6 text-center text-muted-foreground">
                    Brak użytkowników w kontekście tenanta
                  </td>
                </tr>
              ) : (
                query.data.map((user) => (
                  <tr key={user.id} className="border-b border-border hover:bg-muted/60">
                    <td className="px-3 py-1.5">{user.email}</td>
                    <td className="px-3 py-1.5">{user.display_name}</td>
                    <td className="px-3 py-1.5 font-mono text-xs text-muted-foreground">{user.id}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      ) : null}
    </div>
  )
}
