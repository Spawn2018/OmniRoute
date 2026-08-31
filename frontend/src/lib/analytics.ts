const POSTHOG_KEY = import.meta.env.VITE_POSTHOG_KEY as string | undefined
const POSTHOG_HOST = (import.meta.env.VITE_POSTHOG_HOST as string | undefined) ?? "https://eu.i.posthog.com"

type PosthogClient = {
  init: (key: string, options: Record<string, unknown>) => void
  capture: (event: string, properties?: Record<string, string | number | boolean>) => void
}

let initialized = false
let posthogClient: PosthogClient | null = null

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
      person_profiles: "identified_only",
      capture_pageview: true,
    })
    initialized = true
    ph.capture("app_loaded")
  })
}

export function track(event: string, properties?: Record<string, string | number | boolean>): void {
  if (!initialized || !posthogClient) {
    return
  }
  posthogClient.capture(event, properties)
}
