# Machine — nowa tabela: RLS i izolacja

**Status:** machine. Orakulum: `python scripts/quality/craft_close.py --check`.
Nie jest zasadą w AGENTS.md. Nie edytuje GROUNDING.md.

## Sygnał

Migracja w `backend/alembic/versions/` z `op.create_table` w tym samym
commicie co plaster, bez `FORCE ROW LEVEL SECURITY` albo bez pliku
`test_*isolation*`.

## Zamiast

1. `organization_id` na tabeli.
2. `ALTER TABLE … FORCE ROW LEVEL SECURITY`.
3. Test izolacji w `backend/tests/<bc>/` — wzorzec
   `backend/tests/inbound_messages/test_inbound_message_isolation.py`.
4. Kontrakt serwisu: `assert "FORCE ROW LEVEL SECURITY" in source`.

## Zakaz

- Tabela biznesowa bez RLS „na później”.
- Izolacja tylko w komentarzu.
- Dopisywanie HC do AGENTS zamiast testu.
