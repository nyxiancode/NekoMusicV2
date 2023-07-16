import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from NekoMusic import LOGGER, app, userbot
from NekoMusic.core.call import Alexa
from NekoMusic.plugins import ALL_MODULES
from NekoMusic.utils.database import get_banned_users, get_gbanned

loop = asyncio.get_event_loop()


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("NekoMusic").error("Add Pyrogram string session and then try...")
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("NekoMusic.plugins" + all_module)
    LOGGER("NekoMusic.plugins").info("Necessary Modules Imported Successfully.")
    await userbot.start()
    await Alexa.start()
    try:
        await Alexa.stream_call("https://telegra.ph/file/b60b80ccb06f7a48f68b5.mp4")
    except NoActiveGroupCall:
        LOGGER("NekoMusic").error(
            "[ERROR] - \n\nTurn on group voice chat and don't put it off otherwise I'll stop working thanks."
        )
        sys.exit()
    except:
        pass
    await Alexa.decorators()
    LOGGER("NekoMusic").info("Music Bot Started Successfully")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("NekoMusic").info("Stopping Music Bot")
