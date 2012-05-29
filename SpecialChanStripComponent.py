

from _Framework.ChannelStripComponent import ChannelStripComponent 
TRACK_FOLD_DELAY = 5
class SpecialChanStripComponent(ChannelStripComponent):
    ' Subclass of channel strip component using select button for (un)folding tracks '

    def __init__(self):
        ChannelStripComponent.__init__(self)
        self._toggle_fold_ticks_delay = -1
        self._register_timer_callback(self._on_timer)


    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        ChannelStripComponent.disconnect(self)


    def _select_value(self, value):
        ChannelStripComponent._select_value(self, value)
        if (self.is_enabled() and (self._track != None)):
        
            ##Quirksmode
            if (value == 1):
                if self.application().view.is_view_visible('Detail/Clip'):
                    self.application().view.show_view('Detail/DeviceChain')
                    self.application().view.is_view_visible('Detail/DeviceChain')
                else:
                    self.application().view.show_view('Detail/Clip')
                    self.application().view.is_view_visible('Detail/Clip')
            
            if (self._track.is_foldable and (self._select_button.is_momentary() and (value != 0))):
                self._toggle_fold_ticks_delay = TRACK_FOLD_DELAY
            else:
                self._toggle_fold_ticks_delay = -1


    def _on_timer(self):
        if (self.is_enabled() and (self._track != None)):
            if (self._toggle_fold_ticks_delay > -1):
                assert self._track.is_foldable
                if (self._toggle_fold_ticks_delay == 0):
                    self._track.fold_state = (not self._track.fold_state)
                self._toggle_fold_ticks_delay -= 1
