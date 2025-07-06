from fastapi import APIRouter, Request, HTTPException
import stripe
from sheriff.core.config import settings
from sheriff.core.db import get_db_conn

router = APIRouter()

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event["type"]
    data_object = event["data"]["object"]

    if event_type == "account.updated":
        account_id = data_object["id"]
        charges_enabled = data_object["charges_enabled"]
        conn = get_db_conn()
        c = conn.cursor()
        c.execute("UPDATE recipients SET onboarded = %s WHERE stripe_account_id = %s", (charges_enabled, account_id))
        conn.commit()
        c.close()
        conn.close()

    return {"status": "success"}
