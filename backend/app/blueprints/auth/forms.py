from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class RegistrationForm(FlaskForm):
    """
    Registration form for new users.
    """

    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(
                min=2, max=20, message="Username must be between 2 and 20 characters."
            ),
            Regexp(
                regex=r"^[a-zA-Z0-9](?:[a-zA-Z0-9 ]{0,18})[a-zA-Z0-9]$",
                message="Username can only contain letters, numbers, and spaces.",
            ),
        ],
        render_kw={"placeholder": "Username", "autofocus": "true"},
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email address."),
        ],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(
                min=8,
                message="Password must be at least 8 characters long.",
            ),
            Regexp(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[.!@#%])[a-zA-Z0-9.!@#%]{8,}$",
                message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.",
            ),
        ],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Confirm Password is required."),
            EqualTo("password", message="Passwords do not match."),
        ],
        render_kw={"placeholder": "Confirm Password"},
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """
    Login form for existing users.
    """

    email = StringField(
        "Email",
        validators=[DataRequired(message="Email is required.")],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required.")],
        render_kw={"placeholder": "Password"},
    )
    remember = BooleanField("Remember Me", default=True)
    submit = SubmitField("Login")


class ResetPasswordForm(FlaskForm):
    """
    Reset Password form for existing users.
    """

    email = StringField(
        "Email",
        validators=[DataRequired(message="Email is required.")],
        render_kw={"placeholder": "Email", "autofocus": "true"},
    )
    submit = SubmitField("Reset Password")


class NewPasswordForm(FlaskForm):
    """
    New Password form for existing users.
    """

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(
                min=8,
                message="Password must be at least 8 characters long.",
            ),
            Regexp(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[.!@#%])[a-zA-Z0-9.!@#%]{8,}$",
                message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.",
            ),
        ],
        render_kw={"placeholder": "Password", "autofocus": "true"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Confirm Password is required."),
            EqualTo("password", message="Passwords do not match."),
        ],
        render_kw={"placeholder": "Confirm Password"},
    )
    submit = SubmitField("Reset Password")
