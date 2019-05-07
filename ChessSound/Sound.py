###############################
# MODULE: Chess main class    #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 07/07/2019     #
###############################
from enum import IntEnum


class SoundTypes(IntEnum):
    MOVE = 0,
    TICK = 1,
    MAIN = 2,
    WIN = 3


class Sound:
    def __init__(self, base_ref):
        self.base_ref = base_ref
        self.is_played = True
        self.data_folder = 'ChessSound/data/'
        self.sounds = {}
        self.volume = 1.0

        #add default sounds
        self.sounds[SoundTypes.MAIN] = base_ref.loader.loadSfx(self.data_folder + 'main_sound.mp3')
        self.sounds[SoundTypes.MOVE] = base_ref.loader.loadSfx(self.data_folder + 'move.wav')
        self.sounds[SoundTypes.WIN] = base_ref.loader.loadSfx(self.data_folder + 'win.mp3')

    def play(self, music_type, is_looped=False):
        sound = self.sounds.get(music_type, None)
        if sound is None:
            return
        sound.setLoop(is_looped)
        sound.setVolume(self.volume)
        if sound.status() != sound.PLAYING:
            sound.play()

    def set_volume(self, volume):
        if volume < 0 or volume > 1:
            return
        self.volume = volume
        for sound in self.sounds.values():
            sound.setVolume(self.volume)

    def get_volume(self):
        return self.volume

    def turn_off_all(self):
        for sound in self.sounds.values():
            if sound.status() == sound.PLAYING:
                sound.stop()
