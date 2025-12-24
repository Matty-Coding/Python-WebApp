from app.database.models import db, User, EmailToken
from app.utils.decorators import db_commiter
from werkzeug.security import generate_password_hash
from secrets import token_urlsafe


class UserCRUD:
    """
    CRUD operations for users.
    """

    def __init__(self):
        self._user_model = User
        self.session = db.session

    @db_commiter(db)
    def create(self, username: str, email: str, password: str) -> User:
        """
        Create a new user.
        """
        user = self._user_model(
            username=username, email=email, hash_pwd=generate_password_hash(password)
        )
        self.session.add(user)
        return user

    def get_by_id(self, user_id: int) -> User:
        """
        Get a user by id.
        """
        return self._user_model.query.get(user_id)

    def get_by_email(self, email: str) -> User:
        """
        Get a user by email.
        """
        return self._user_model.query.filter_by(email=email).first()

    @db_commiter(db)
    def update(self, user_id: int, **kwargs) -> User:
        """
        Update a user by id.
        """
        user = self.get_by_id(user_id)

        for key, value in kwargs.items():
            setattr(user, key, value)
        return user

    @db_commiter(db)
    def update_password(self, user_id: int, password: str) -> User:
        """
        Update a user password by id.
        """
        user = self.get_by_id(user_id)
        setattr(user, "hash_pwd", generate_password_hash(password))
        return user

    @db_commiter(db)
    def delete(self, user_id: int) -> None:
        """
        Delete a user by id.
        """
        user = self.get_by_id(user_id)
        self.session.delete(user)


# CRUD operations for email tokens
class EmailTokenCRUD(UserCRUD):
    """
    CRUD operations for email tokens.
    """

    def __init__(self):
        super().__init__()
        self._email_token_model = EmailToken

    @db_commiter(db)
    def create(self, user_id: int) -> EmailToken:
        """
        Create a new email token.
        """
        email_token = self._email_token_model(user_id=user_id, token=token_urlsafe(32))
        self.session.add(email_token)
        return email_token

    def get_by_id(self, user_id: int) -> EmailToken:
        """
        Get a email token by user_id.
        """
        return self._email_token_model.query.filter_by(user_id=user_id).first()

    def get_by_token(self, token: str) -> EmailToken:
        """
        Get a email token by token.
        """
        return self._email_token_model.query.filter_by(token=token).first()

    db_commiter(db)

    def validate_token(self, user_id: int) -> EmailToken:
        """
        Update a email token by user_id.
        """
        email_token = self.get_by_id(user_id)
        setattr(email_token, "used", True)
        return email_token

    @db_commiter(db)
    def delete(self, user_id: int) -> None:
        """
        Delete a email token by user_id.
        """
        email_token = self.get_by_id(user_id)
        self.session.delete(email_token)
