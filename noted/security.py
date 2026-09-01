import re


PASSWORD_MIN_LENGTH = 12


def password_error(password):
    """Return a user-facing password-policy error, or None when valid."""
    if len(password) < PASSWORD_MIN_LENGTH:
        return f"password must be at least {PASSWORD_MIN_LENGTH} characters."

    requirements = (
        (r"[a-z]", "a lowercase letter"),
        (r"[A-Z]", "an uppercase letter"),
        (r"[0-9]", "a number"),
        (r"[^A-Za-z0-9]", "a symbol"),
    )
    missing = [label for pattern, label in requirements if not re.search(pattern, password)]
    if missing:
        return "password must include " + ", ".join(missing) + "."
    return None
