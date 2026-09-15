"""This file is used to generate the short_code using Base62
Now why base62 - comprises of A-Z + a-z + 0-9  (62 characters). This technique includes 
only letters and numbers excluding /,-,+ special characyers.
"""

import secrets
import string

_ALPHABET = string.ascii_letters + string.digits

def generate_short_code(length : int) -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(length)) 