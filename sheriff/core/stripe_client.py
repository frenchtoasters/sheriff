import stripe
from sheriff.core.config import settings

stripe.api_key = settings.stripe_secret_key

# If using stripe-mock for testing
if settings.stripe_api_base:
    stripe.api_base = settings.stripe_api_base
