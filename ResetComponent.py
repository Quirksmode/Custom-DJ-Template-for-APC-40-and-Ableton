from _Framework.ButtonElement import ButtonElement #added
from _Framework.EncoderElement import EncoderElement #added 

class ResetComponent():
	'Resets all the different FX and Controls'
	__module__ = __name__


	def __init__(self, parent):
		self._parent = parent
		self._shift_button = None
		self._shift_pressed = False
		
		


	def reset_track(self, value):
		if value == 1:
			if not self._shift_pressed:
				for device in self._parent.song().view.selected_track.devices:
					for parameter in range(8):
						device.parameters[parameter+1].value = (value * 0)
						if(device.name == "DJ EQ and FX"):
							if (parameter <= 3):
								device.parameters[parameter+1].value = (value * 127)
							if (parameter == 4):
								device.parameters[4].value = (value * 64)
						elif(device.name == "Scratcher"):			
							device.parameters[parameter+1].value = (value * 0)
							device.parameters[1].value = (value * 25)
							device.parameters[3].value = (value * 54)
							device.parameters[4].value = (value * 80)
							device.parameters[5].value = (value * 90)
							
	
	def reset_all(self, value):
		if value == 1:
			for track_index in range(8):
				for device in self._parent.song().tracks[track_index].devices:
					for parameter in range(8):
						device.parameters[parameter+1].value = (value * 0)
						if(device.name == "DJ EQ and FX"):
							if (parameter <= 3):
								device.parameters[parameter+1].value = (value * 127)
							if (parameter == 4):
								device.parameters[4].value = (value * 64)
						elif(device.name == "Scratcher"):
							device.parameters[1].value = (value * 25)			
							device.parameters[3].value = (value * 54)
							device.parameters[4].value = (value * 80)
							device.parameters[5].value = (value * 90)
							  


	def set_shift_button(self, button): #added
		assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
		if (self._shift_button != button):
			if (self._shift_button != None):
				self._shift_button.remove_value_listener(self._shift_value)
			self._shift_button = button
			if (self._shift_button != None):
				self._shift_button.add_value_listener(self._shift_value)

	def _shift_value(self, value): #added
		assert (self._shift_button != None)
		assert (value in range(128))
		self._shift_pressed = (value != 0)