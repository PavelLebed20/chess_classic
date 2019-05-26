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
        self.sounds[SoundTypes.MAIN] = [base_ref.loader.loadSfx(self.data_folder + 'main_sound.mp3'), True]
        self.sounds[SoundTypes.MOVE] = [base_ref.loader.loadSfx(self.data_folder + 'move.wav'), True]
        self.sounds[SoundTypes.WIN] = [base_ref.loader.loadSfx(self.data_folder + 'win.mp3'), True]


    def play(self, music_type, is_looped=False):
        sound = self.sounds.get(music_type, None)
        if sound is None:
            return
        if sound[1] is False:
            return
        sound[0].setLoop(is_looped)
        sound[0].setVolume(self.volume)
        if sound[0].status() != sound[0].PLAYING:
            sound[0].play()

    def set_volume(self, volume):
        if volume < 0 or volume > 1:
            return
        self.volume = volume
        for sound in self.sounds.values():
            sound[0].setVolume(self.volume)

    def get_volume(self):
        return self.volume

    def turn_off_all(self):
        for sound in self.sounds.values():
            if sound[0].status() == sound[0].PLAYING:
                sound[0].stop()

    def turn(self, music_type, to_play):
        if music_type not in self.sounds:
            return
        sound = self.sounds.get(music_type, None)
        if sound is None:
            return
        sound[1] = to_play
        if to_play is False and sound[0].status() == sound[0].PLAYING:
            sound[0].stop()

    def can_play(self, music_type):
        if music_type not in self.sounds:
            return False
        return self.sounds[music_type][1]

