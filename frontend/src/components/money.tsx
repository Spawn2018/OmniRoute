import { formatMoney, moneyAxis } from "@/lib/money"

type MoneyProps = {
  amount: string
  currency: string
}

export function Money({ amount, currency }: MoneyProps) {
  const axis = moneyAxis(amount, currency)
  if (axis === null) {
    return <span className="tabular-nums">{formatMoney(amount, currency)}</span>
  }
  return (
    <span className="money-axis" data-money="axis">
      <span className="money-axis-int">{axis.integer}</span>
      <span className="money-axis-frac">.{axis.fraction}</span>
      <span className="money-axis-ccy">{axis.currency}</span>
    </span>
  )
}
