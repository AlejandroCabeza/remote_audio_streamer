# Python Imports
import asyncio
from threading import Thread
# Third-Party Imports
# Project Imports
from gui.gui_application import GuiApplication
from audio.engine.audio_engine_factory import AudioEngineFactory
from discord_client.models import DiscordClient
from discord_client.settings import BOT_TOKEN, ROOT_PATH_MUSIC_LIBRARY


class App:

    def __init__(self):
        self.event_loop = asyncio.get_event_loop()
        self.discord_client: DiscordClient = DiscordClient(BOT_TOKEN, self.event_loop)
        self.audio_engine_factory: AudioEngineFactory = AudioEngineFactory(self.discord_client)
        self.gui: GuiApplication = GuiApplication(self.event_loop, ROOT_PATH_MUSIC_LIBRARY, self.audio_engine_factory)
        self.thread = Thread(target=self._run_event_loop_processes)

    def _run_event_loop_processes(self):
        asyncio.set_event_loop(self.event_loop)
        asyncio.get_event_loop().run_until_complete(self.discord_client.start())

    def start(self):
        self.thread.start()
        self.gui.exec_()

    def stop(self):
        asyncio.run_coroutine_threadsafe(self.stop_background_services(), self.event_loop)
        self.thread.join()

    async def stop_background_services(self):
        await self.discord_client.close()
        await self.gui.audio_engine.audio_client.disconnect()

    def run(self):
        self.start()
        self.stop()


if __name__ == '__main__':
    App().run()
