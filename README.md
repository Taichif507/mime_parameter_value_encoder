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

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

## Contributing

Issues and pull requests are welcome. Please keep the dependency list empty —
that constraint is the point of the project, not an oversight.

