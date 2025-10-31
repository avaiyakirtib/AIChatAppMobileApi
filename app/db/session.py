from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# When using Render's managed PostgreSQL, a simpler engine configuration is needed.
# The complex parameters for Supabase's external pooler are no longer required.
# We will use the DATABASE_URL directly from your environment variables.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Still a good practice to detect and handle dead connections
)

# SessionLocal will now use the new, simplified engine configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

