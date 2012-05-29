
from _Framework.EncoderElement import EncoderElement 
from _Framework.ButtonElement import ButtonElement 
RING_OFF_VALUE = 0
RING_SIN_VALUE = 1
RING_VOL_VALUE = 2
RING_PAN_VALUE = 3
class RingedEncoderElement(EncoderElement):
    ' Class representing a continuous control on the controller enclosed with an LED ring '

    def __init__(self, msg_type, channel, identifier, map_mode):
        EncoderElement.__init__(self, msg_type, channel, identifier, map_mode)
        self._ring_mode_button = None
        self.set_needs_takeover(False)


    def set_ring_mode_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._ring_mode_button != None):
            force_send = True
            self._ring_mode_button.send_value(RING_OFF_VALUE, force_send)
        self._ring_mode_button = button
        self._update_ring_mode()


    def connect_to(self, parameter):
        if ((parameter != self._parameter_to_map_to) and (not self.is_mapped_manually())):
            force_send = True
            self._ring_mode_button.send_value(RING_OFF_VALUE, force_send)
        EncoderElement.connect_to(self, parameter)


    def release_parameter(self):
        EncoderElement.release_parameter(self)
        self._update_ring_mode()


    def install_connections(self):
        EncoderElement.install_connections(self)
        if ((not self._is_mapped) and (len(self._value_notifications) == 0)):
            self._is_being_forwarded = self._install_forwarding(self)
        self._update_ring_mode()


    def is_mapped_manually(self):
        return ((not self._is_mapped) and (not self._is_being_forwarded))


    def _update_ring_mode(self):
        if (self._ring_mode_button != None):
            force_send = True
            if self.is_mapped_manually():
                self._ring_mode_button.send_value(RING_SIN_VALUE, force_send)
            elif (self._parameter_to_map_to != None):
                param = self._parameter_to_map_to
                p_range = (param.max - param.min)
                value = (((param.value - param.min) / p_range) * 127)
                self.send_value(int(value), force_send)
                if (self._parameter_to_map_to.min == (-1 * self._parameter_to_map_to.max)):
                    self._ring_mode_button.send_value(RING_PAN_VALUE, force_send)
                elif self._parameter_to_map_to.is_quantized:
                    self._ring_mode_button.send_value(RING_SIN_VALUE, force_send)
                else:
                    self._ring_mode_button.send_value(RING_VOL_VALUE, force_send)
            else:
                self._ring_mode_button.send_value(RING_OFF_VALUE, force_send)

