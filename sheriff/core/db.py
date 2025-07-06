import psycopg2
from psycopg2.extras import RealDictCursor
from sheriff.core.config import settings

def get_db_conn():
    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        cursor_factory=RealDictCursor
    )

def init_db():
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS recipients (
            id SERIAL PRIMARY KEY,
            discord_id TEXT UNIQUE,
            email TEXT,
            stripe_account_id TEXT,
            onboarded BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    c.close()
    conn.close()
