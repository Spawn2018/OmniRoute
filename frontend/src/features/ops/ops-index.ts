import { BUSINESS_LISTS } from "@/lib/business-lists"

export const ADMIN_REF_SURFACES = [
  "sidebar-density",
  "table-toolbar",
  "command-actions",
] as const

export const OPS_JOBS = [
  { route: BUSINESS_LISTS.extractions.route, label: "Ekstrakcje HITL", job: "extract / accept" },
  {
    route: BUSINESS_LISTS.financeBoard.route,
    label: "Tablica finansowa",
    job: "odczyt marży / NBP / limitu / recenzji",
  },
  {
    route: BUSINESS_LISTS.salesInvoice.route,
    label: "Faktury",
    job: "sell z charge do zafakturowania",
  },
  {
    route: BUSINESS_LISTS.quoteInvoiceSettlement.route,
    label: "Rozliczenie wyceny",
    job: "wycena i sell po rate_line_id",
  },
  {
    route: BUSINESS_LISTS.bankPayment.route,
    label: "Bank i płatności",
    job: "IBAN kontrahenta i sell z charge",
  },
  {
    route: BUSINESS_LISTS.moneyCost.route,
    label: "Koszt pieniądza",
    job: "NBP i buy z charge",
  },
  {
    route: BUSINESS_LISTS.fxDifference.route,
    label: "Różnice kursowe",
    job: "NBP walut z charge i wyceny",
  },
  {
    route: BUSINESS_LISTS.cashFlow.route,
    label: "Przepływy",
    job: "wypływ buy i wpływ sell z charge",
  },
  {
    route: BUSINESS_LISTS.costToServe.route,
    label: "Koszt obsługi klienta",
    job: "SOP i wyceny wybranego kontrahenta",
  },
  {
    route: BUSINESS_LISTS.bookkeeping.route,
    label: "Księgowość",
    job: "nazwa charge_code oraz buy/sell",
  },
  {
    route: BUSINESS_LISTS.roadTransport.route,
    label: "Transport drogowy",
    job: "lokalizacje postal_zone i address",
  },
  {
    route: BUSINESS_LISTS.intermodalRail.route,
    label: "Kolej intermodalna",
    job: "porty z flagą rail",
  },
  {
    route: BUSINESS_LISTS.chinaRail.route,
    label: "Kolej z Chin",
    job: "porty CN z flagą rail",
  },
  {
    route: BUSINESS_LISTS.oceanLcl.route,
    label: "Drobnica morska",
    job: "porty z is_seaport",
  },
  {
    route: BUSINESS_LISTS.sanctions.route,
    label: "Sankcje",
    job: "aktywni kontrahenci tax_id i kraj",
  },
  {
    route: BUSINESS_LISTS.mailIntegration.route,
    label: "Poczta",
    job: "odczyt domen i kontaktów",
  },
  {
    route: BUSINESS_LISTS.operatorNotice.route,
    label: "Powiadomienia",
    job: "HITL pending i wyceny pending",
  },
  {
    route: BUSINESS_LISTS.shipment.route,
    label: "Zlecenia",
    job: "wyceny z party_id jako praca handlowa",
  },
  {
    route: BUSINESS_LISTS.tracking.route,
    label: "Tracking",
    job: "lane POL/POD z wyceny",
  },
  {
    route: BUSINESS_LISTS.operationalException.route,
    label: "Wyjątki",
    job: "wyceny z party bez pełnego POL/POD",
  },
  {
    route: BUSINESS_LISTS.shipmentDocument.route,
    label: "Dokumenty zlecenia",
    job: "source_ref wycen z party_id",
  },
  {
    route: BUSINESS_LISTS.ediMessage.route,
    label: "EDI",
    job: "channel_quote na lane wyceny",
  },
  { route: BUSINESS_LISTS.chargeCodes.route, label: "Kody opłat", job: "katalog charge_code" },
  {
    route: BUSINESS_LISTS.commodityCodes.route,
    label: "Kody towarowe",
    job: "katalog commodity_code",
  },
  {
    route: BUSINESS_LISTS.dangerousGoods.route,
    label: "Towary niebezpieczne",
    job: "katalog dangerous_good UN/IMDG",
  },
  {
    route: BUSINESS_LISTS.networks.route,
    label: "Sieci",
    job: "katalog network per tenant",
  },
  {
    route: BUSINESS_LISTS.nbpRates.route,
    label: "Kursy NBP",
    job: "katalog nbp_rate tabeli A",
  },
  { route: BUSINESS_LISTS.rateLines.route, label: "Stawki kupna", job: "rate_line + source_ref" },
  { route: BUSINESS_LISTS.charges.route, label: "Opłaty", job: "buy+sell / marża" },
  {
    route: BUSINESS_LISTS.channelQuotes.route,
    label: "Oferty kanału",
    job: "katalog channel_quote + resolve",
  },
  {
    route: BUSINESS_LISTS.quotations.route,
    label: "Wyceny",
    job: "SQL z rate_line + kanał + zapytania",
  },
  { route: BUSINESS_LISTS.organizationSettings.route, label: "Ustawienia", job: "config jako dane" },
  { route: BUSINESS_LISTS.ports.route, label: "Porty", job: "katalog UN/LOCODE + resolve" },
  {
    route: BUSINESS_LISTS.portSurcharges.route,
    label: "Opłaty portowe",
    job: "katalog port_surcharge + resolve",
  },
  {
    route: BUSINESS_LISTS.locations.route,
    label: "Lokalizacje",
    job: "strefy taryfowe + resolve kodu",
  },
  {
    route: BUSINESS_LISTS.terminals.route,
    label: "Terminale",
    job: "katalog ISPS + resolve",
  },
  {
    route: BUSINESS_LISTS.parties.route,
    label: "Kontrahenci",
    job: "katalog party + resolve tax_id / mail",
  },
  {
    route: BUSINESS_LISTS.partyScorecards.route,
    label: "Karty wyników",
    job: "snapshot party_scorecard",
  },
  {
    route: BUSINESS_LISTS.customerSops.route,
    label: "Procedury klienta",
    job: "katalog customer_sop + zatwierdzenie",
  },
  {
    route: BUSINESS_LISTS.creditReviews.route,
    label: "Recenzje kredytowe",
    job: "katalog credit_review + resolve",
  },
  { route: BUSINESS_LISTS.users.route, label: "Użytkownicy", job: "tenant users" },
  { route: "/session", label: "Sesja", job: "token klienta" },
] as const

export const HELLO_DASHBOARD_MARKERS = ["Shell 0.5", "hello-dashboard", "kafelki"] as const

export const SHIPPED_CHARGE_ROUTES = {
  "1.0": "/charge-codes",
  "1.1": "/rate-lines",
  "1.2": "/charges",
  "2.0": "/quotations",
  "3.0": "/organization-settings",
  "4.0": "/ports",
  "4.1": "/locations",
  "4.2": "/terminals",
  "5.0": "/parties",
  "5.2": "/commodity-codes",
  "6.0": "/nbp-rates",
  "7.0": "/dangerous-goods",
  "8.0": "/parties",
  "9.0": "/networks",
  "10.0": "/party-scorecards",
  "11.0": "/customer-sops",
  "12.0": "/port-surcharges",
  "13.0": "/channel-quotes",
  "14.0": "/credit-reviews",
  "15.0": "/finance",
  "16.0": "/quotations",
  "17.0": "/quotations",
  "18.0": "/quotations",
  "19.0": "/quotations",
  "20.0": "/quotations",
  "21.0": "/quotations",
  "22.0": "/quotations",
  "23.0": "/quotations",
  "24.0": "/quotations",
  "25.0": "/mail",
  "26.0": "/mail",
  "27.0": "/notifications",
  "28.0": "/shipments",
  "29.0": "/tracking",
  "30.0": "/exceptions",
  "31.0": "/shipment-documents",
  "32.0": "/edi",
  "33.0": "/invoices",
  "34.0": "/quote-invoices",
  "35.0": "/payments",
  "36.0": "/money-cost",
  "37.0": "/fx-differences",
  "38.0": "/cashflows",
  "39.0": "/cost-to-serve",
  "40.0": "/bookkeeping",
  "41.0": "/road",
  "42.0": "/rail",
  "43.0": "/china-rail",
  "44.0": "/lcl",
  "45.0": "/sanctions",
} as const

export const ROUTES_BREADTH_STANDING =
  "Nowe BC z jobem operatora = trasa w tym samym plasterze. Charge 1.0–1.2 już mają UI. To standing, nie 70 modułów."
