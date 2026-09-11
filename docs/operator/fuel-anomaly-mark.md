# Fuel anomaly (EXP2.14)

Operator zapisuje etykietę karty paliwowej, zbiornika albo skoku zużycia. To katalog
HITL, nie silnik anomalii.

Wiersz ma `mark_code`, `anomaly_kind` i `source_ref`. System nie łączy się z kartą
paliwową, nie czyta telemetry zbiornika i nie mnoży indeksu FSC.

Live fuel anomaly / karta paliwowa zostają leftoverem poza tym plasterem.
