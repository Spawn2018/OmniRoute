import { OPS_JOBS } from "@/features/ops/ops-index"

type OpsIndexProps = {
  healthLabel: string
  healthState: "loading" | "ok" | "down"
}

export function OpsIndex({ healthLabel, healthState }: OpsIndexProps) {
  return (
    <div className="space-y-2" data-admin-ref="ops-index">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-sm font-semibold">Praca operatora</h2>
        <p
          data-admin-ref="health"
          className={healthState === "down" ? "text-xs text-destructive" : "text-xs text-muted-foreground"}
        >
          API {healthLabel}
        </p>
      </div>
      <p className="text-xs text-muted-foreground">
        Gęsty admin · sidebar compact · toolbar tabeli · ⌘K akcje. Bez pustych modułów.
      </p>
      <table className="w-full border-collapse text-sm">
        <thead className="bg-muted text-left text-xs text-muted-foreground">
          <tr className="border-b border-border">
            <th className="px-2 py-1 font-medium">Ekran</th>
            <th className="px-2 py-1 font-medium">Job</th>
            <th className="px-2 py-1 font-medium">Trasa</th>
          </tr>
        </thead>
        <tbody>
          {OPS_JOBS.map((job) => (
            <tr key={job.route} className="border-b border-border">
              <td className="px-2 py-1">
                <a className="underline" href={job.route}>
                  {job.label}
                </a>
              </td>
              <td className="px-2 py-1 text-xs text-muted-foreground">{job.job}</td>
              <td className="px-2 py-1 font-mono text-xs">{job.route}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
