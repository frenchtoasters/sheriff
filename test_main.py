
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock
from stripe.error import SignatureVerificationError
from sheriff.main import app

# ---------- Async client fixture ----------
@pytest_asyncio.fixture
async def async_client():
    with patch("sheriff.core.db.init_db") as mock_init_db:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

# ---------- Test /health ----------
@pytest.mark.asyncio
async def test_health(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# ---------- Test /create_recipient ----------
@pytest.mark.asyncio
@patch("sheriff.api.routes_recipients.get_db_conn")
@patch("sheriff.api.routes_recipients.stripe.Account.create")
@patch("sheriff.api.routes_recipients.stripe.AccountLink.create")
async def test_create_recipient(mock_accountlink_create, mock_account_create, mock_db_conn, async_client):
    # Mock Stripe account creation
    mock_account_create.return_value = MagicMock(id="acct_test123")

    # Mock Stripe AccountLink creation
    mock_accountlink_create.return_value = MagicMock(url="https://stripe.com/onboard/link")

    # Mock DB connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    payload = {
        "discord_id": "123456",
        "email": "test@example.com"
    }

    response = await async_client.post("/create_recipient", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["account_id"] == "acct_test123"
    assert "onboarding_link" in data

# ---------- Test /recipients ----------
@pytest.mark.asyncio
@patch("sheriff.api.routes_recipients.get_db_conn")
async def test_list_recipients(mock_db_conn, async_client):
    # Mock DB connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"discord_id": "123", "email": "a@b.com", "stripe_account_id": "acct_123", "onboarded": True}
    ]
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = await async_client.get("/recipients")
    assert response.status_code == 200
    data = response.json()
    assert "recipients" in data
    assert isinstance(data["recipients"], list)

# ---------- Test /webhook with account.updated ----------
@pytest.mark.asyncio
@patch("sheriff.api.routes_webhook.get_db_conn")
@patch("sheriff.api.routes_webhook.stripe.Webhook.construct_event")
async def test_webhook_account_updated(mock_construct_event, mock_db_conn, async_client):
    # Mock Stripe webhook event
    mock_construct_event.return_value = {
        "type": "account.updated",
        "data": {
            "object": {
                "id": "acct_test123",
                "charges_enabled": True
            }
        }
    }

    # Mock DB connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    payload = {}
    headers = {"stripe-signature": "valid_sig"}

    response = await async_client.post("/webhook", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

# ---------- Test /webhook with invalid signature ----------
@pytest.mark.asyncio
@patch("sheriff.api.routes_webhook.stripe.Webhook.construct_event")
async def test_webhook_invalid_signature(mock_construct_event, async_client):
    mock_construct_event.side_effect = SignatureVerificationError("Invalid signature", "sig_header")

    payload = {}
    headers = {"stripe-signature": "bad_sig"}

    response = await async_client.post("/webhook", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid signature"

