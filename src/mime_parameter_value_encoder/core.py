"""Core encoding logic for RFC 2231 parameter continuations."""

import urllib.parse


def _needs_encoding(value: str) -> bool:
    """True if *value* contains characters that require RFC 2231 encoding.

    Only printable ASCII minus the RFC-2045 tspecial set may appear bare.
    Anything else — control chars, high bytes, or tspecials — forces encoding.
    We encode the whole value rather than mixing bare and %-encoded chars so
    the caller always gets a single self-consistent string.
    """
    tspecials = set("()<>@,;:\\\"/[]?=")
    for ch in value:
        code = ord(ch)
        if code <= 32 or code >= 127:
            return True
        if ch in tspecials:
            return True
    return False


def encode_parameter_value(value: str, charset: str = "utf-8") -> str:
    """Encode a parameter value for an RFC 2231 continuation segment.

    Parameters
    ----------
    value:
        Raw value to encode. Must be a ``str``.
    charset:
        Character set used when the value needs encoding. Defaults to
        ``"utf-8"``.

    Returns
    -------
    str
        If *value* is already safe as a bare token, it is returned unchanged
        so the caller can place it directly after ``*=`` without quotes. If
        *value* contains non-ASCII or RFC-2045 tspecial characters, the result
        is an RFC-2231 single-segment value of the form
        ``charset'language'encoded`` where *encoded* is percent-encoded.

    Notes
    -----
    Language is always empty. Multi-segment continuation (the
    ``*0``, ``*1`` indexing for long values) is not handled here — this
    function produces a single segment only, which is the common case for
    filenames.
    """
    if not isinstance(value, str):
        raise TypeError("value must be str")
    if not isinstance(charset, str):
        raise TypeError("charset must be str")
    if charset == "":
        raise ValueError("charset must not be empty")

    if not _needs_encoding(value):
        return value

    raw_bytes = value.encode(charset)
    # urllib.parse.quote percent-encodes each non-safe byte, which matches the
    # RFC-2231 percent-encoding rule for continuation values.
    encoded = urllib.parse.quote(raw_bytes, safe="")
    return "{}''{}".format(charset, encoded)
