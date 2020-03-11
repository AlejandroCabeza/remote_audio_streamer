# Python Imports
from pathlib import Path
# Third-Party Imports
# Project Imports
from utils.environment import get_environment_variable_or_error


BOT_TOKEN: str = get_environment_variable_or_error("BOT_TOKEN")
CHANNEL_ID_DND: int = int(get_environment_variable_or_error("CHANNEL_ID_DND"))
CHANNEL_ID_LAREIRA: int = int(get_environment_variable_or_error("CHANNEL_ID_LAREIRA"))
ROOT_PATH_MUSIC_LIBRARY: Path = Path(get_environment_variable_or_error("ROOT_PATH_MUSIC_LIBRARY"))
