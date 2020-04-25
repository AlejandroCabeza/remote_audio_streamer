# Python Imports
from io import BytesIO
# Third-Party Imports
# Project Imports
from audio.buffer.audio_buffer_interfaces import IAudioBuffer
from audio.utils.ffmpeg import get_raw_audio_data_from_audio_file


class SynchronousAudioBuffer(IAudioBuffer):

    def __init__(self, audio_file_path: str, channels: int, sampling_rate: int, raw_data_frame_size: int):
        self._raw_data_frame_size: int = raw_data_frame_size
        self._raw_data_audio_buffer: BytesIO = BytesIO(
            get_raw_audio_data_from_audio_file(audio_file_path, channels, sampling_rate)
        )
        self._bytes_amount = self._raw_data_audio_buffer.getbuffer().nbytes
        self._frames_amount = self._bytes_amount / self._raw_data_frame_size

    def read(self) -> bytes:
        raw_audio_bytes: bytes = self._raw_data_audio_buffer.read(self._raw_data_frame_size)
        if self._do_audio_bytes_need_padding(raw_audio_bytes):
            raw_audio_bytes = self._pad_audio_bytes(raw_audio_bytes)
        return raw_audio_bytes

    def _do_audio_bytes_need_padding(self, audio_bytes: bytes) -> bool:
        return len(audio_bytes) not in (0, self._raw_data_frame_size)

    def _pad_audio_bytes(self, audio_bytes: bytes) -> bytes:
        return audio_bytes.ljust(self._raw_data_frame_size, b'\x00')

    def get_pointer_position_as_percentage(self) -> float:
        frame_index: int = int(self._get_pointer_position() / self._raw_data_frame_size)
        return frame_index / self._frames_amount * 100

    def _get_pointer_position(self) -> int:
        return self._raw_data_audio_buffer.tell()

    def set_pointer_position_from_percentage(self, percentage: float):
        self._raw_data_audio_buffer.seek(self._get_byte_position_from_percentage(percentage))

    def _get_byte_position_from_percentage(self, percentage: float) -> int:
        return self._raw_data_frame_size * self._get_frame_index_from_percentage(percentage)

    def _get_frame_index_from_percentage(self, percentage: float) -> int:
        return int(self._frames_amount * percentage / 100)
