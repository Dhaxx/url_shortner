import secrets
import string

ALPHABET = string.ascii_letters + string.digits
DEFAULT_LENGTH = 7

class ShortCodeGenerator:
    @staticmethod
    def generate(length: int = DEFAULT_LENGTH) -> str:
        return "".join(
            secrets.choice(ALPHABET)
            for _ in range(length)
        )