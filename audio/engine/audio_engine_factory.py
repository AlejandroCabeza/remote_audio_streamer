# Python Imports
# Third-Party Imports
# Project Imports
from discord_client.settings import CHANNEL_ID_LAREIRA
from audio.engine.audio_engine_interfaces import IObservableAudioEngine
from audio.engine.discord_audio_engine import DiscordAudioEngine


class AudioEngineFactory:

    def __init__(self, discord_client):
        self.discord_client = discord_client

    async def create_observable_audio_engine(self) -> IObservableAudioEngine:
        await self.discord_client.wait_until_ready()
        return DiscordAudioEngine(
            await self.discord_client.connect_to_voice_client(CHANNEL_ID_LAREIRA)
        )
