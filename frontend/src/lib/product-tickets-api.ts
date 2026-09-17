import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ProductTicketRow = {
  id: string
  organization_id: string
  ticket_code: string
  title: string
  body: string
  ticket_kind: string
  source_ref: string
}

export type ProductTicketPayload = {
  ticket_code: string
  title: string
  body: string
  ticket_kind: string
  source_ref: string
}

const PATH = "/api/v1/product-tickets"

export function buildProductTicketWrite(args: {
  code: string
  title: string
  body: string
  kind: string
  origin: string
}): ProductTicketPayload {
  return {
    ticket_code: args.code.trim(),
    title: args.title.trim(),
    body: args.body.trim(),
    ticket_kind: args.kind.trim(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchProductTickets(): Promise<ProductTicketRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać ticketów produktu"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as ProductTicketRow[]
}

export async function saveProductTicket(
  payload: ProductTicketPayload,
): Promise<ProductTicketRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "product-ticket-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać ticketu produktu"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as ProductTicketRow
}
