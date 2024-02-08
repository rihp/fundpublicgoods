from dataclasses import dataclass
from uuid import UUID
from fund_public_goods.db.app_db import create_admin
from fund_public_goods.db.entities import FundingEntries


@dataclass(kw_only=True)
class FundingEntryData:
    project_id: str
    amount: float
    token: str
    weight: float

def exists(run_id: str):
    try:
        db = create_admin()
        entries = db.table("funding_entries").select("id").eq("run_id", run_id).execute()
        return len(entries.data) > 0
    except:
        return False


def insert_multiple(run_id: str, entries: list[FundingEntryData]):
    db = create_admin()
    if exists(run_id):
        delete_from_run(run_id)

    db.table("funding_entries").insert(
        [
            {
                "run_id": run_id,
                "project_id": row.project_id,
                "amount": row.amount,
                "token": row.token,
                "weight": row.weight
            }
            for row in entries
        ]
    ).execute()

def delete_from_run(run_id):
    db = create_admin()
    db.table("funding_entries").delete().eq("run_id", run_id).execute()

def add_transaction_hash(id: str, hash: str):
    db = create_admin()
    db.table("funding_entries").update({ "transaction_hash": hash }).eq("id", id).execute()
