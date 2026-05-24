"""
WebWorld
"""
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


from .constants import *
from .options import cartogr_ap_option_groups


class CartogrAPWebWorld(WebWorld):
    game: str = GAME_NAME
    theme: str = WEB_WORLD_THEME

    setup_en: Tutorial = Tutorial(
        tutorial_name=EN_TUTORIAL_NAME,
        description=EN_TUTORIAL_DESC,
        language=EN_TUTORIAL_LANGUAGE,
        file_name=EN_TUTORIAL_FILENAME,
        link=EN_TUTORIAL_LINK,
        authors=EN_TUTORIAL_AUTHORS,
    )
    tutorials: list[Tutorial] = [setup_en]
    option_groups = cartogr_ap_option_groups




