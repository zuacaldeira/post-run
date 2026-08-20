"""HTTP against PowerCenter.

This is a private API. There is no published documentation, no developer
programme, and no terms that say what is allowed -- what exists publicly is
other people's reverse engineering, and the endpoints below come from a working
client rather than from a spec. Two consequences worth holding onto:

  * it can change or vanish without notice, so every call here fails loudly
    rather than papering over a shape it did not expect, and
  * we are a guest. The calendar route returns the entire history in one
    response, so there is never a reason to poll it. Fetch it weekly at most.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://www.stryd.com/b/api/v1"
TIMEOUT_S = 30
USER_AGENT = "postrun-sync (+https://postrun.zuacaldeira.com)"


class ApiError(RuntimeError):
    """A request failed. Carries the status and the path, never the token."""


class Unauthorized(ApiError):
    """401/403 -- almost always an expired token rather than a wrong one."""


def get(path: str, tok: str, params: dict[str, Any] | None = None) -> dict:
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", "Bearer " + tok)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", USER_AGENT)

    # One retry, and only for the failures a retry can actually fix. Retrying a
    # 401 just means asking twice with a credential we already know is stale.
    last: Exception | None = None
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as res:
                body = res.read()
            break
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                raise Unauthorized(
                    "PowerCenter refused the token ({}). It has most likely "
                    "expired -- copy a fresh one from local storage.".format(exc.code)
                ) from None
            if exc.code < 500 or attempt == 2:
                raise ApiError("GET {} -> HTTP {}".format(path, exc.code)) from None
            last = exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 2:
                raise ApiError("GET {} -> {}".format(path, exc.__class__.__name__)) from None
            last = exc
    else:                                                   # pragma: no cover
        raise ApiError("GET {} failed: {}".format(path, last))

    try:
        parsed = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ApiError(
            "GET {} returned {} bytes that are not JSON. The API has probably "
            "changed shape, or this is a sign-in page.".format(path, len(body))
        ) from exc

    if not isinstance(parsed, dict):
        raise ApiError("GET {} returned {}, expected an object".format(path, type(parsed).__name__))
    return parsed


def calendar(tok: str, athlete: str) -> dict:
    """The whole plan, past and future, in one response."""
    return get("/users/{}/calendar".format(athlete), tok)
