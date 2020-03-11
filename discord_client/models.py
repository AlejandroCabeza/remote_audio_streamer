# Python Imports
import discord
from discord import VoiceClient
# Third-Party Imports
# Project Imports
from discord_client.settings import CHANNEL_ID_LAREIRA


class DiscordClient(discord.Client):

    def __init__(self, token=None, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.token = token
        self.voice_client = None

    async def start(self):
        await super().start(self.token)

    async def on_message(self, message):
        if message.content.startswith("/roll"):
            await message.channel.send("WIP")

    async def on_ready(self):
        print("Discord Client service started.")

    async def connect_to_voice_client(self, channel_id: int) -> VoiceClient:
        return await self.get_channel(channel_id).connect()
