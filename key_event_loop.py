import chara_loop
import chip_loop
from config import current_config
from chording_modes import ChordingModes


def key_loop(key_queue):
    if current_config.mode == ChordingModes.CHARA_CHORDER:
        chara_loop.chara_key_loop(key_queue)
    elif current_config.mode == ChordingModes.FUZZY_CHIPS:
        chip_loop.chip_key_loop(key_queue)
