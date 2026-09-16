const POSTHOG_KEY = import.meta.env.VITE_POSTHOG_KEY as string | undefined
const POSTHOG_HOST = (import.meta.env.VITE_POSTHOG_HOST as string | undefined) ?? "https://eu.i.posthog.com"

export const EXTRACT_ACCEPT_EVENTS = [
  "extraction_draft_created",
  "extraction_draft_accepted",
  "extraction_draft_rejected",
  "extraction_draft_patched",
  "extraction_draft_undone",
] as const

export type ExtractAcceptEvent = (typeof EXTRACT_ACCEPT_EVENTS)[number]

const ALLOWED = new Set<string>(EXTRACT_ACCEPT_EVENTS)

type PosthogClient = {
  init: (key: string, options: Record<string, unknown>) => void
  capture: (event: string, properties?: Record<string, string | number | boolean>) => void
}

let initialized = false
let posthogClient: PosthogClient | null = null

export function isExtractAcceptEvent(event: string): event is ExtractAcceptEvent {
  return ALLOWED.has(event)
}

async function loadPosthog(): Promise<PosthogClient | null> {
  if (!POSTHOG_KEY) {
    return null
  }
  if (posthogClient) {
    return posthogClient
  }
  const mod = await import("posthog-js")
  posthogClient = mod.default
  return posthogClient
}

export function initAnalytics(): void {
  if (initialized || !POSTHOG_KEY) {
    return
  }
  void loadPosthog().then((ph) => {
    if (!ph || initialized || !POSTHOG_KEY) {
      return
    }
    ph.init(POSTHOG_KEY, {
      api_host: POSTHOG_HOST,
      person_profiles: "never",
      capture_pageview: false,
      disable_session_recording: true,
    })
    initialized = true
  })
}

export function track(event: string, properties?: Record<string, string | number | boolean>): void {
  if (!initialized || !posthogClient) {
    return
  }
  if (!isExtractAcceptEvent(event)) {
    return
  }
  if (properties !== undefined) {
    return
  }
  posthogClient.capture(event)
}
