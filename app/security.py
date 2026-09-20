from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

password_hasher = PasswordHasher()


def hash_password(password):
    return password_hasher.hash(password)


def verify_password(password, hashed_password):
    try:
        password_hasher.verify(hashed_password, password)
        return True
    except (InvalidHashError, VerificationError, VerifyMismatchError):
        return False