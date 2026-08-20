"""The credential, and nothing else.

**No password ever reaches this code.** PowerCenter authenticates with email and
password and hands back a JWT; that exchange is deliberately not implemented
here, because handling a password in plain text is a line this project does not
cross. Obtaining the token is the athlete's job:

    sign in at stryd.com in a browser
    DevTools -> Application -> Local Storage -> https://www.stryd.com
    copy the JWT
    write it to the token file and chmod 600

The token expires. When it does, repeat: nothing here can renew it, and nothing
here should try, because renewing it means holding the password.

The token is never printed, logged, or included in an error message. The one
thing worth saying out loud is *where* the file should be, never what was in it.
"""

from __future__ import annotations

import base64
import binascii
import json
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PATH = Path(os.environ.get("STRYD_TOKEN_FILE", "/etc/postrun/stryd.token"))

HOW_TO_GET_ONE = (
    "Stryd needs a PowerCenter session token. It never needs your password.\n"
    "  1. sign in at https://www.stryd.com\n"
    "  2. DevTools -> Application -> Local Storage -> https://www.stryd.com\n"
    "  3. copy the JWT and write it to {path}\n"
    "  4. chmod 600 {path}\n"
    "The token expires; when it does, repeat."
)


class MissingToken(RuntimeError):
    """No token where one was expected. Says where to put one, never what was read."""


class ExpiredToken(RuntimeError):
    """The token parsed but its own `exp` has passed."""


def read(path: Path | None = None) -> str:
    """The token, from the environment or from a file outside the repo."""
    env = os.environ.get("STRYD_TOKEN")
    if env and env.strip():
        return env.strip()

    path = path or DEFAULT_PATH
    try:
        raw = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise MissingToken(HOW_TO_GET_ONE.format(path=path)) from exc
    if not raw:
        raise MissingToken(HOW_TO_GET_ONE.format(path=path))
    return raw


def claims(tok: str) -> dict:
    """The JWT's payload.

    Read, not verified. We are not the audience for this token and hold no key
    to check it with -- Stryd verifies it, and a token we mangled would simply
    be refused. The claims are read for two practical things: saying "expired"
    before making a request that would 401, and finding the athlete id without
    a second round trip.
    """
    parts = tok.split(".")
    if len(parts) != 3:
        return {}
    body = parts[1] + "=" * (-len(parts[1]) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(body).decode("utf-8"))
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError):
        return {}


def expires_at(tok: str) -> datetime | None:
    exp = claims(tok).get("exp")
    if not isinstance(exp, (int, float)):
        return None
    return datetime.fromtimestamp(exp, tz=timezone.utc)


def is_expired(tok: str, *, now: datetime | None = None) -> bool:
    when = expires_at(tok)
    if when is None:
        return False          # no exp claim: let the API be the judge
    return when <= (now or datetime.now(timezone.utc))


def athlete_id(tok: str) -> str:
    """The user id the calendar route is keyed on.

    It is already inside the credential, so asking the API who we are would be a
    round trip to learn something we were handed.
    """
    c = claims(tok)
    for key in ("sub", "id", "user_id", "userId", "uid"):
        v = c.get(key)
        if isinstance(v, (str, int)) and str(v).strip():
            return str(v).strip()
    raise MissingToken(
        "The token carries no user id claim, so the calendar route cannot be "
        "addressed. Re-copy the JWT from local storage; a truncated paste is "
        "the usual cause."
    )
