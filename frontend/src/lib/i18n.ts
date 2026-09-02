const PL_MESSAGES = {
  "extraction_quality.title": "Jakość ekstrakcji",
  "extraction_quality.subtitle":
    "extraction_quality M-69 · unparsed_regions · nie scoring · nie accept",
  "tenant_rollout.title": "Wdrożenie tenanta",
  "tenant_rollout.subtitle": "tenant_rollout M-70 · default_currency · nie tabela · nie upsert",
} as const

export type UiMessageKey = keyof typeof PL_MESSAGES

const PL_INSTANT = new Intl.DateTimeFormat("pl-PL", {
  dateStyle: "short",
  timeStyle: "short",
  timeZone: "Europe/Warsaw",
})

function isUiMessageKey(key: string): key is UiMessageKey {
  return Object.hasOwn(PL_MESSAGES, key)
}

export function t(key: string): string {
  if (!isUiMessageKey(key)) {
    throw new Error(`brak klucza i18n: ${key}`)
  }
  return PL_MESSAGES[key]
}

export function formatInstant(iso: string): string {
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(iso)) {
    return ""
  }
  const instant = new Date(iso)
  if (instant.toString() === "Invalid Date") {
    return ""
  }
  return PL_INSTANT.format(instant)
}
