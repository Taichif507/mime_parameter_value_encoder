"""Tests for mime_parameter_value_encoder.core."""

import unittest

from mime_parameter_value_encoder import encode_parameter_value


class TestEncodeParameterValue(unittest.TestCase):

    def test_ascii_safe_returned_verbatim(self):
        self.assertEqual(encode_parameter_value("report.pdf"), "report.pdf")

    def test_space_triggers_encoding(self):
        # SPACE (0x20) is below the printable threshold, so full encoding kicks in.
        self.assertEqual(
            encode_parameter_value("my file.txt"),
            "utf-8''my%20file.txt",
        )

    def test_tspecial_triggers_encoding(self):
        # semicolon is a tspecial and must not appear bare
        self.assertEqual(
            encode_parameter_value("a;b"),
            "utf-8''a%3Bb",
        )

    def test_quote_tspecial(self):
        self.assertEqual(
            encode_parameter_value('a"b'),
            "utf-8''a%22b",
        )

    def test_non_ascii_utf8(self):
        # café → c(0x63) a(0x61) f(0x66) é(0xC3 0xA9)
        self.assertEqual(
            encode_parameter_value("caf\u00e9"),
            "utf-8''caf%C3%A9",
        )

    def test_custom_charset_iso_8859_1(self):
        # é is 0xE9 in ISO-8859-1
        self.assertEqual(
            encode_parameter_value("caf\u00e9", charset="iso-8859-1"),
            "iso-8859-1''caf%E9",
        )

    def test_empty_string_safe(self):
        # No characters means no encoding needed.
        self.assertEqual(encode_parameter_value(""), "")

    def test_del_encoded(self):
        # DEL (0x7F) is a control character and should be encoded.
        self.assertEqual(
            encode_parameter_value("\x7f"),
            "utf-8''%7F",
        )

    def test_control_char_encoded(self):
        # newline (0x0A) is a control char → encode
        self.assertEqual(
            encode_parameter_value("a\nb"),
            "utf-8''a%0Ab",
        )

    def test_non_str_value_raises(self):
        with self.assertRaises(TypeError):
            encode_parameter_value(b"bytes")  # type: ignore[arg-type]

    def test_non_str_charset_raises(self):
        with self.assertRaises(TypeError):
            encode_parameter_value("ok", charset=123)  # type: ignore[arg-type]

    def test_empty_charset_raises(self):
        with self.assertRaises(ValueError):
            encode_parameter_value("ok", charset="")


if __name__ == "__main__":
    unittest.main()
