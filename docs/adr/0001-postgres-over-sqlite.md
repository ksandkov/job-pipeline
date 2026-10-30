# ADR 0001: Postgres over SQLite

## Status
Accepted

## Context
The app runs in k3s with potential concurrent writers (pipeline + API) and needs
real indexing and a `/readyz` that means something.

## Decision
Postgres 16 (via SQLAlchemy + psycopg). SQLite stays only as a possibility for
throwaway local runs.

## Consequences
- Concurrency and indexing are handled properly.
- One more stateful component to run and back up.
