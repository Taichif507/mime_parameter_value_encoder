"""mime_parameter_value_encoder

Encodes non-ASCII parameter values in RFC 2231 continuation segments
for Content-Disposition headers.
"""

from .core import encode_parameter_value

__all__ = ["encode_parameter_value"]
