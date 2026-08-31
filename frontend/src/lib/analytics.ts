import posthog from "posthog-js"

const POSTHOG_KEY = import.meta.env.VITE_POSTHOG_KEY as string | undefined
const POSTHOG_HOST = (import.meta.env.VITE_POSTHOG_HOST as string | undefined) ?? "https://eu.i.posthog.com"

let initialized = false

export function initAnalytics(): void {
  if (initialized || !POSTHOG_KEY) {
    return
  }
  posthog.init(POSTHOG_KEY, {
    api_host: POSTHOG_HOST,
    person_profiles: "identified_only",
    capture_pageview: true,
  })
  initialized = true
  posthog.capture("app_loaded")
}

export function track(event: string, properties?: Record<string, string | number | boolean>): void {
  if (!initialized) {
    return
  }
  posthog.capture(event, properties)
}
