import { Link } from "@tanstack/react-router"
import { cn } from "@/lib/utils"

const NAV = [
  { to: "/", label: "Pulpit" },
  { to: "/tenancy/users", label: "Użytkownicy" },
  { to: "/extractions", label: "Ekstrakcje" },
  { to: "/charge-codes", label: "Kody opłat" },
  { to: "/charges", label: "Opłaty" },
  { to: "/rate-lines", label: "Stawki" },
  { to: "/session", label: "Sesja" },
] as const

export function Sidebar({ currentPath }: { currentPath: string }) {
  return (
    <aside className="flex w-52 shrink-0 flex-col border-r border-border bg-sidebar text-sidebar-foreground">
      <div className="border-b border-border px-3 py-3">
        <div className="text-sm font-semibold tracking-tight">OmniRoute</div>
        <div className="text-xs text-muted-foreground">ops · compact</div>
      </div>
      <nav className="flex flex-col gap-0.5 p-2">
        {NAV.map((item) => {
          const active = currentPath === item.to
          return (
            <Link
              key={item.to}
              to={item.to}
              aria-current={active ? "page" : undefined}
              className={cn(
                "rounded-md px-2 py-1.5 text-sm hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                active && "bg-muted font-medium",
              )}
            >
              {item.label}
            </Link>
          )
        })}
      </nav>
      <div className="mt-auto border-t border-border px-3 py-2 text-xs text-muted-foreground">
        Ctrl+K · paleta
      </div>
    </aside>
  )
}
