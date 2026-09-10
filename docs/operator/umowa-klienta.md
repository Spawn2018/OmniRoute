# Umowa klienta

Na `/customer-contracts` dopisujesz **nagłówek umowy** tenanta: kod snake oraz etykiety załadowcy i odbiorcy. Opcjonalnie zaznaczasz fixture blob. To nie treść umowy, nie PDF i nie szyfr.

1. Wejdź na Umowa klienta. Wpisz kod (`acme_pl_2026` — snake 2–32).
2. Wpisz etykietę załadowcy i etykietę odbiorcy (tekst, nie identyfikator kontrahenta).
3. Podaj `source_ref` (`fixture://contract/…` albo `tenant:manual`).
4. Opcjonalnie zaznacz „dołącz fixture blob”. Lista pokaże Tak albo Nie w kolumnie Opakowanie. Bajty nie wracają na ekran.
5. „Zapisz nagłówek umowy”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: treść umowy, PDF, unwrap, podgląd bajtów, KEK, klauzula SLA, kara, live p44/FourKites/Shippeo, extract LLM. Marża zostaje na `/charges`.

Nazwy w kodzie: `customer_contract` · `contract_code` · `shipper_label` · `their_customer_label` · `source_ref` · `has_ciphertext`.
