# Dopłata lokalna

Na `/local-charges` zapisujesz **dopłatę** THC, ISPS, seal albo amendment z kwotą Decimal.
Opcjonalnie podajesz port UN/LOCODE, typ ISO kontenera, etykietę armatora i serwisu liniowego.
To nie extra portowe i nie warning braku.

1. Wejdź na Dopłaty lokalne. Wybierz rodzaj, kwotę i walutę ISO.
2. Zero i float odpadają. Nieznany rodzaj odpada.
3. Port zostaw pusty, gdy dopłata nie jest związana z jednym UN/LOCODE. Zły kod (nie 5 znaków) odpada.
4. Typ ISO (np. `22G1`) zostaw pusty, gdy dopłata nie jest na jeden rozmiar pudła. Zły token (nie 4 znaki ISO) odpada. To nie numer BIC i nie FK do katalogu kontenerów.
5. Armator i serwis liniowy zostaw puste, gdy dopłata nie jest na jedną linię. To tekst HITL do 64 znaków, nie FK do `party` i nie live HTTP.
6. „Zapisz dopłatę lokalną” z `source_ref` (`fixture://local-charge/…` albo `tenant:manual`).

Czego tu nie ma: FK do katalogu portów/kontenerów/party, warning braków jako fakt, zapis na `charge`.
Marża zostaje na `/charges`. Extra portowe zostają na `/port-surcharges`.

Stance ostrzeżenia braku dopłaty (ostrzeż / wstrzymaj / zwolnij / inne) zapisujesz osobno na
`/local-charge-warning-marks`. To nie silnik braków i nie 409 na wycenie.

Stance wiązania dopłaty do charge/quote (charge / quote / other) zapisujesz na
`/local-charge-bind-marks`. To nie FK UUID i nie matching SQL.

Nazwy w kodzie: `local_charge` · `charge_kind` · `port_unlocode` · `iso_size_type` · `carrier_label` · `service_label` · `amount` · `currency` · `source_ref` · `local_charge_warning_mark` · `warning_kind` · `local_charge_bind_mark` · `bind_kind`.
