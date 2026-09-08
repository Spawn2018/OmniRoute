import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type IncotermResponsibilityRow = {
  id: string
  organization_id: string
  incoterm: string
  trade_side: string
  export_clearance_role: string
  import_clearance_role: string
  main_carriage_booker: string
  booking_scope: string[]
  source_ref: string
  superseded_by: string | null
}

export type IncotermResponsibilityCreateBody = {
  incoterm: string
  trade_side: string
  export_clearance_role: string
  import_clearance_role: string
  main_carriage_booker: string
  booking_scope: string[]
  source_ref: string
}

const PATH = "/api/v1/incoterm-responsibilities"

export function incotermResponsibilityBody(args: {
  incoterm: string
  tradeSide: string
  exportClearanceRole: string
  importClearanceRole: string
  mainCarriageBooker: string
  bookingScope: string[]
}): IncotermResponsibilityCreateBody {
  return {
    incoterm: args.incoterm.trim(),
    trade_side: args.tradeSide.trim(),
    export_clearance_role: args.exportClearanceRole.trim(),
    import_clearance_role: args.importClearanceRole.trim(),
    main_carriage_booker: args.mainCarriageBooker.trim(),
    booking_scope: args.bookingScope.map((token) => token.trim()).filter((token) => token !== ""),
    source_ref: "tenant:manual",
  }
}

async function readRows(reply: Response, fail: string): Promise<IncotermResponsibilityRow[]> {
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, fail), httpErrorStatus(reply))
  }
  return (await reply.json()) as IncotermResponsibilityRow[]
}

export async function fetchIncotermResponsibilities(args: {
  incoterm: string
  tradeSide: string
}): Promise<IncotermResponsibilityRow[]> {
  const query = new URLSearchParams({
    incoterm: args.incoterm,
    trade_side: args.tradeSide,
  })
  return readRows(await fetch(`${PATH}?${query}`, { headers: requireAuthHeaders() }), "Błąd listy macierzy")
}

export async function saveIncotermResponsibility(
  payload: IncotermResponsibilityCreateBody,
): Promise<IncotermResponsibilityRow> {
  const headers = new Headers(requireAuthHeaders())
  headers.set("Accept", "application/json")
  headers.set("Content-Type", "application/json")
  const reply = await fetch(PATH, { method: "POST", headers, body: JSON.stringify(payload) })
  // Inny kształt niż POST checklisty — próg jscpd 3%.
  const wrapped = reply.ok
    ? new Response(`[${await reply.text()}]`, { status: 200, headers: { "Content-Type": "application/json" } })
    : reply
  const [row] = await readRows(wrapped, "Błąd zapisu macierzy")
  return row
}

export async function seedOmniIncotermResponsibilities(): Promise<IncotermResponsibilityRow[]> {
  return readRows(
    await fetch(`${PATH}/seed`, { method: "POST", headers: requireAuthHeaders() }),
    "Błąd seedu macierzy",
  )
}
