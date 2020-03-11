# Python Imports
import audioop
# Third-Party Imports
# Project Imports


def apply_volume_to_bytes(audio_bytes: bytes, volume: float) -> bytes:
    return audioop.mul(audio_bytes, 2, volume)
