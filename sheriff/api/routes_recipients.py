from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import stripe
from sheriff.core.config import settings
from sheriff.core.db import get_db_conn

router = APIRouter()

class OnboardRequest(BaseModel):
    discord_id: str
    email: str

@router.post("/create_recipient")
async def create_recipient(req: OnboardRequest):
    try:
        account = stripe.Account.create(
            type="express",
            country="US",
            email=req.email,
            capabilities={"transfers": {"requested": True}},
        )
        conn = get_db_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO recipients (discord_id, email, stripe_account_id, onboarded)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (discord_id) DO UPDATE
            SET email = EXCLUDED.email,
                stripe_account_id = EXCLUDED.stripe_account_id
        """, (req.discord_id, req.email, account.id, False))
        conn.commit()
        c.close()
        conn.close()

        account_link = stripe.AccountLink.create(
            account=account.id,
            refresh_url=settings.refresh_url,
            return_url=settings.return_url,
            type="account_onboarding",
        )

        return {
            "message": "Recipient created and onboarding link generated",
            "onboarding_link": account_link.url,
            "account_id": account.id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/recipients")
async def list_recipients():
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT discord_id, email, stripe_account_id, onboarded FROM recipients")
    rows = c.fetchall()
    c.close()
    conn.close()
    return {"recipients": rows}
