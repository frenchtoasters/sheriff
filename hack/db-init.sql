CREATE TABLE IF NOT EXISTS recipients (
    id SERIAL PRIMARY KEY,
    discord_id TEXT UNIQUE,
    email TEXT,
    stripe_account_id TEXT,
    onboarded BOOLEAN DEFAULT FALSE
);
