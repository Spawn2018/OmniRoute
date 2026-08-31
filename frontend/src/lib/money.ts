export type MoneyPair = {
  amount: string
  currency: string
}

const CURRENCY_RE = /^[A-Z]{3}$/
const CANONICAL_RE = /^-?\d{1,10}(?:\.\d{1,4})?$/
const MAX_ABS = 10_000_000_000n

function rejectFloat(amount: unknown): void {
  if (typeof amount === "number") {
    throw new Error("kwota nie może być float")
  }
}

function normalizeDecimalText(amount: string): string | null {
  const trimmed = amount.trim()
  if (trimmed === "") {
    return null
  }
  const hasComma = trimmed.includes(",")
  const hasDot = trimmed.includes(".")
  if (hasComma && hasDot) {
    return null
  }
  return hasComma ? trimmed.replace(",", ".") : trimmed
}

function scaleToFourPlaces(normalized: string): string | null {
  if (!CANONICAL_RE.test(normalized)) {
    return null
  }
  const negative = normalized.startsWith("-")
  const unsigned = negative ? normalized.slice(1) : normalized
  const [whole, fraction = ""] = unsigned.split(".")
  const digits = whole === "0" ? 0n : BigInt(whole)
  if (digits >= MAX_ABS) {
    return null
  }
  const frac4 = `${fraction}0000`.slice(0, 4)
  return `${negative ? "-" : ""}${whole}.${frac4}`
}

export function parseMoney(amount: string, currency: string): MoneyPair | null {
  rejectFloat(amount)
  if (typeof amount !== "string" || typeof currency !== "string") {
    return null
  }
  if (!CURRENCY_RE.test(currency)) {
    return null
  }
  const normalized = normalizeDecimalText(amount)
  if (normalized === null) {
    return null
  }
  const scaled = scaleToFourPlaces(normalized)
  if (scaled === null) {
    return null
  }
  return { amount: scaled, currency }
}

export function formatMoney(amount: string, currency: string): string {
  const parsed = parseMoney(amount, currency)
  if (parsed === null) {
    return `${amount} ${currency}`
  }
  return `${parsed.amount} ${parsed.currency}`
}
