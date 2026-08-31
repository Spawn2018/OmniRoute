import { formatMoney } from "@/lib/money"

type MoneyProps = {
  amount: string
  currency: string
}

export function Money({ amount, currency }: MoneyProps) {
  return <span className="tabular-nums">{formatMoney(amount, currency)}</span>
}
