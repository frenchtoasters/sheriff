import os
import yaml
import stripe

class Settings:
    def __init__(self):
        with open("sheriff-config.yaml", "r") as f:
            config = yaml.safe_load(f)

        env = config["environment"]

        if env == "local":
            stripe_config = config["stripe"]
            db = config["database"]
            urls = config["urls"]

            self.stripe_secret_key = stripe_config["secret_key"]
            self.stripe_webhook_secret = stripe_config["webhook_secret"]
            self.db_host = db["host"]
            self.db_port = db["port"]
            self.db_name = db["name"]
            self.db_user = db["user"]
            self.db_password = db["password"]
            self.refresh_url = urls["refresh_url"]
            self.return_url = urls["return_url"]
            self.stripe_api_base = stripe_config.get("api_base") or None
        else:
            self.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
            self.stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
            self.db_host = os.getenv("DB_HOST")
            self.db_port = os.getenv("DB_PORT", "5432")
            self.db_name = os.getenv("DB_NAME")
            self.db_user = os.getenv("DB_USER")
            self.db_password = os.getenv("DB_PASSWORD")
            self.refresh_url = os.getenv("REFRESH_URL")
            self.return_url = os.getenv("RETURN_URL")
            self.stripe_api_base = os.getenv("STRIPE_API_BASE")

        # Initialize Stripe globally here
        stripe.api_key = self.stripe_secret_key

        if self.stripe_api_base:
            stripe.api_base = self.stripe_api_base

settings = Settings()

