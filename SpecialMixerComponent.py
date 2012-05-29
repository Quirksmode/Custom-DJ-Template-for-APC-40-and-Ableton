
from _Framework.MixerComponent import MixerComponent 
from SpecialChanStripComponent import SpecialChanStripComponent 
class SpecialMixerComponent(MixerComponent):
    ' Special mixer class that uses return tracks alongside midi and audio tracks '

    def __init__(self, parent, num_tracks):
        self._parent = parent #added
        MixerComponent.__init__(self, num_tracks)
        self._shift_button = None #added
        self._shift_pressed = False #added


    def tracks_to_use(self):
        return (self.song().visible_tracks + self.song().return_tracks)


    def _create_strip(self):
        return SpecialChanStripComponent()
