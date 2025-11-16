from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

Base = declarative_base()

_engine = None
SessionLocal = None

def init_db(app):
    global _engine, SessionLocal
    if _engine is not None:
        return _engine

    db_url = app.config["SQLALCHEMY_DATABASE_URI"]
    engine_options = app.config.get("SQLALCHEMY_ENGINE_OPTIONS", {})

    _engine = create_engine(db_url, **engine_options)
    SessionLocal = scoped_session(
        sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    )

    @app.teardown_appcontext
    def remove_session(exception=None):
        SessionLocal.remove()

    return _engine


def get_session():
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return SessionLocal()
