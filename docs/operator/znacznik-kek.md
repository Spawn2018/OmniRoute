# Znacznik KEK

Na `/tenant-contract-keks` dopisujesz **znacznik owijki** tenanta: kod snake oraz token `password` albo `kms`. To nie jest klucz. 273.0 nadal nie jest szyfrowaniem.

1. Wejdź na Znacznik KEK. Wpisz kod (`desk_wrap_pl` — snake 2–32).
2. Wybierz rodzaj owijki: `password` albo `kms`. To etykieta sposobu, nie hasło i nie wywołanie KMS.
3. Podaj `source_ref` (`fixture://kek/…` albo `tenant:manual`).
4. „Zapisz znacznik KEK”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: materiał klucza, hasło, ciphertext, unwrap, KMS, `wrapped_dek`, Fernet, kolumny sekretu na umowie, klauzula SLA, live p44/FourKites/Shippeo, extract LLM. Marża zostaje na `/charges`. Umowa zostaje na `/customer-contracts`.

Nazwy w kodzie: `tenant_contract_kek` · `kek_code` · `wrap_kind` · `source_ref`.
