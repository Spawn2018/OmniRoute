import { Link } from "@tanstack/react-router"
import { cn } from "@/lib/utils"

const NAV = [
  { to: "/", label: "Pulpit" },
  { to: "/tenancy/users", label: "Użytkownicy" },
  { to: "/extractions", label: "Ekstrakcje" },
  { to: "/charge-codes", label: "Kody opłat" },
  { to: "/charges", label: "Opłaty" },
  { to: "/rate-lines", label: "Stawki" },
  { to: "/quotations", label: "Wyceny" },
  { to: "/ports", label: "Porty" },
  { to: "/organization-settings", label: "Ustawienia" },
  { to: "/session", label: "Sesja" },
] as const

export function Sidebar({ currentPath }: { currentPath: string }) {
  return (
    <aside
      data-admin-ref="sidebar-density"
      className="flex w-44 shrink-0 flex-col border-r border-border bg-sidebar text-sidebar-foreground"
    >
      <div className="border-b border-border px-2 py-1.5">
        <div className="text-sm font-semibold tracking-tight">OmniRoute</div>
        <div className="text-[11px] text-muted-foreground">gęsty admin</div>
      </div>
      <nav className="flex flex-col gap-px p-1">
        {NAV.map((item) => {
          const active = currentPath === item.to
          return (
            <Link
              key={item.to}
              to={item.to}
              aria-current={active ? "page" : undefined}
              className={cn(
                "rounded-md px-2 py-1 text-xs hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                active && "bg-muted font-medium",
              )}
            >
              {item.label}
            </Link>
          )
        })}
      </nav>
      <div className="mt-auto border-t border-border px-2 py-1.5 text-[11px] text-muted-foreground">
        ⌘K · akcje operatora
      </div>
    </aside>
  )
}
