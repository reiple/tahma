from __future__ import annotations

from .config import SUPPORTED_ENCODINGS

IAC = 255


def strip_telnet_commands(data: bytes) -> bytes:
    """Remove basic Telnet negotiation sequences while preserving user text."""
    output = bytearray()
    index = 0
    while index < len(data):
        byte = data[index]
        if byte != IAC:
            output.append(byte)
            index += 1
            continue

        if index + 1 >= len(data):
            break
        command = data[index + 1]

        if command == IAC:
            output.append(IAC)
            index += 2
        elif command in (251, 252, 253, 254):  # WILL, WONT, DO, DONT
            index += 3
        elif command in (250,):  # SB ... SE
            index += 2
            while index + 1 < len(data) and not (data[index] == IAC and data[index + 1] == 240):
                index += 1
            index += 2
        else:
            index += 2
    return bytes(output)


def decode_client_line(data: bytes, preferred_encoding: str) -> tuple[str, str]:
    cleaned = strip_telnet_commands(data).strip(b"\r\n\x00")
    candidates = (preferred_encoding, *[enc for enc in SUPPORTED_ENCODINGS if enc != preferred_encoding])
    for encoding in candidates:
        try:
            return cleaned.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return cleaned.decode(preferred_encoding, errors="replace"), preferred_encoding


def encode_server_text(text: str, encoding: str) -> bytes:
    return text.encode(encoding, errors="replace")
