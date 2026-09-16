import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type InboundMessage = {
  id: string
  organization_id: string
  source_ref: string
  from_address: string
  subject: string
  body_text: string
  status: string
  party_id: string | null
  external_id: string | null
  rfc822_message_id: string | null
  in_reply_to: string | null
}

export function inboundMessageCreateBody(input: {
  source_ref: string
  from_address: string
  subject: string
  body_text: string
  rfc822_message_id?: string
  in_reply_to?: string
}): {
  source_ref: string
  from_address: string
  subject: string
  body_text: string
  rfc822_message_id?: string
  in_reply_to?: string
} {
  const body: {
    source_ref: string
    from_address: string
    subject: string
    body_text: string
    rfc822_message_id?: string
    in_reply_to?: string
  } = {
    source_ref: input.source_ref.trim(),
    from_address: input.from_address.trim(),
    subject: input.subject.trim(),
    body_text: input.body_text.trim(),
  }
  const messageId = input.rfc822_message_id?.trim() ?? ""
  const replyTo = input.in_reply_to?.trim() ?? ""
  if (messageId !== "") {
    body.rfc822_message_id = messageId
  }
  if (replyTo !== "") {
    body.in_reply_to = replyTo
  }
  return body
}

async function readInboundMessage(
  response: Response,
  fallback: string,
): Promise<InboundMessage> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as InboundMessage
}

export async function fetchInboundMessages(): Promise<InboundMessage[]> {
  const response = await fetch("/api/v1/inbound-messages", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy wiadomości"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as InboundMessage[]
}

export async function createInboundMessage(body: {
  source_ref: string
  from_address: string
  subject: string
  body_text: string
  rfc822_message_id?: string
  in_reply_to?: string
}): Promise<InboundMessage> {
  const response = await fetch("/api/v1/inbound-messages", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readInboundMessage(response, "Błąd zapisu wiadomości")
}

export async function extractInboundMessage(messageId: string): Promise<{
  id: string
  status: string
  source_ref: string
}> {
  const response = await fetch(`/api/v1/inbound-messages/${messageId}/extract`, {
    method: "POST",
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd extract z wiadomości"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as { id: string; status: string; source_ref: string }
}

type InboundKeyedIngest = {
  external_id: string
  source_ref: string
  from_address: string
  subject: string
  body_text: string
}

async function postKeyedInboundMessage(
  path: "/api/v1/inbound-messages/ingest-graph" | "/api/v1/inbound-messages/ingest-imap",
  body: InboundKeyedIngest,
  fallback: string,
): Promise<InboundMessage> {
  const response = await fetch(path, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readInboundMessage(response, fallback)
}

export function ingestMailboxInboundMessage(
  body: InboundKeyedIngest,
): Promise<InboundMessage> {
  return postKeyedInboundMessage(
    "/api/v1/inbound-messages/ingest-imap",
    body,
    "Błąd ingestu skrzynki",
  )
}

export function ingestGraphInboundMessage(
  body: InboundKeyedIngest,
): Promise<InboundMessage> {
  return postKeyedInboundMessage(
    "/api/v1/inbound-messages/ingest-graph",
    body,
    "Błąd ingestu Graph",
  )
}

export async function resolveInboundMessageEmail(
  messageId: string,
): Promise<InboundMessage> {
  const response = await fetch(`/api/v1/inbound-messages/${messageId}/resolve-email`, {
    method: "POST",
    headers: requireAuthHeaders(),
  })
  return readInboundMessage(response, "Błąd dopasowania nadawcy")
}
