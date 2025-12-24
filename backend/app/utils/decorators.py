from functools import wraps
from flask import current_app


def db_commiter(db):
    """
    Decorator to commit or rollback changes to the database and log the result.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                db.session.flush()
                db.session.commit()
                current_app.logger.info(f"✅  {func.__name__} commited.")
                return result

            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"⚠️  {func.__name__} failed to commit: {e}")
                raise

        return wrapper

    return decorator
