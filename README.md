# mime_parameter_value_encoder

Encodes non-ASCII parameter values in RFC 2231 continuation segments for `Content-Disposition` headers.

```python
from mime_parameter_value_encoder import encode_parameter_value

segment = encode_parameter_value("café-report.pdf")
# → "utf-8''caf%C3%A9-report.pdf"
header = f"Content-Disposition: attachment; filename*=UTF-8''{segment}"
```

## Why

Browsers expect `Content-Disposition` filenames containing non-ASCII bytes to
be percent-encoded per RFC 2231, with a `charset'language'` prefix. This
library produces that single-segment value. Values that are already safe
printable-ASCII tokens are returned verbatim so the caller can place them
after `*=` without extra quoting.

The trade-off: only single-segment encoding is supported. If a filename is
long enough to need RFC-2231 line-folding across `*0`, `*1`, … segments,
this library does not split it — the caller must handle segment indexing.

## Edge cases

A SPACE or any RFC-2045 tspecial character (`()<>@,;:"/[]?=`) triggers full
encoding of the entire value, even if the rest is ASCII. The library never
mixes bare and percent-encoded characters in one segment, which keeps the
output predictable for every parser.
