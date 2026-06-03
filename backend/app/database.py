import time
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database(max_attempts: int = 20) -> None:
    from app import models  # noqa: F401

    last_error: Exception | None = None
    for _ in range(max_attempts):
        try:
            with engine.begin() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            Base.metadata.create_all(bind=engine)
            return
        except Exception as exc:  # pragma: no cover - startup retry path
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"Database initialization failed: {last_error}")
