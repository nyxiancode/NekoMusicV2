import random
from NekoMusic.utils.database import get_theme

themes = [
    "neko1",
    "neko2",
    "neko3",
    "neko4",
    "neko5",
    "neko6",
    "neko7",
    "neko8",
]


async def check_theme(chat_id: int):
    _theme = await get_theme(chat_id, "theme")
    if not _theme:
        theme = random.choice(themes)
    else:
        theme = _theme["theme"]
        if theme == "Random":
            theme = random.choice(themes)
    return theme
