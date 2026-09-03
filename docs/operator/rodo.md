# RODO

Inwentarz na `/gdpr` to konta tenanta (`email`, `display_name`). Wniosek zapisujesz osobno — to ślad, nie kasowanie bazy.

1. Wejdź na RODO. Skopiuj `id` konta z listy albo z `/tenancy/users`.
2. Wklej `app_user_id`, wybierz rodzaj `access` albo `erasure` i `source_ref` (`fixture://gdpr-request/…` albo `tenant:manual`).
3. „Zapisz wniosek” otwiera wiersz. Drugi otwarty wniosek tego samego rodzaju na to samo konto odrzuca.
4. „Wypełnij” przy `access` tylko zamyka wniosek — lista kont **jest** udostępnieniem, bez pliku ZIP.
5. „Wypełnij” przy `erasure` zamienia email na tombstone, nazwę na „usunięte” i czyści hasło. Wiersza konta nie kasuje (inne tabele trzymają `created_by`).

Czego tu nie ma: DPIA, zgody, kasowanie maili i kontrahentów, portal osoby. Marża zostaje na `/charges`.

Nazwy w kodzie: `gdpr_request` · `request_kind` · `app_user_id` · `source_ref`.
