from _Framework.ButtonElement import ButtonElement #added
from _Framework.EncoderElement import EncoderElement #added
from _Framework.ButtonMatrixElement import ButtonMatrixElement



class SceneEffectComponent():
	'Handles Scene Launch Button Effects'
	__module__ = __name__
	
	def __init__(self, parent):
	
		self._parent = parent
		self._rack = []
		self._reset = []
		self._device_buttons = []
		self._masterRepeat_button = None
		self._newStopAll_button = None
		self._shift_button = None
		self._shift_pressed = False
		self._holdToggle = True
		self._lightToggle = False
		self._amount = 0
		
		for index in range(self._parent._trackTotal):
			self._rack.append(False)
			
		
		
		
		for track in range(self._parent._trackTotal):
			for device in parent.song().tracks[track].devices:
				if device.name == "Scene Launch Effects":
					self._rack[track] = device
					break
		
		
		
		## List to set the button light
		self._repeat_stateList = [False, False, False, False, False]
		self._repeat_allStateList = []
		for index in range(self._parent._trackTotal):
			self._repeat_allStateList.append(self._repeat_stateList)
		
		## List to set the Effect Mode button light
		self._effectMode_stateList = [True, False, False, False, False]
		self._effectMode_allStateList = []
		for index in range(self._parent._trackTotal):
			self._effectMode_allStateList.append(self._effectMode_stateList)
			
		## List to remember each tracks chosen Effect
		self._effectSelect_stateList = [2, 2, 2, 2, 2, 2, 2, 2]
		
    		
		
		
		self._parent.current_track = 0
		self._parent.song().view.add_selected_track_listener(self.sceneLight)
		self._effectSelect = 2
		self._paramValues = [25, 50, 80, 110, 127]
		self._effectMessage = [
		"########################################################################################## EFFECT: REPEAT ROLL ##########################", 
		"########################################################################################## EFFECT: REPEATS ##############################",
		"########################################################################################## EFFECT: GATER ##############################",
		"########################################################################################## EFFECT: BEAT MASHER ##########################",
		"########################################################################################## EFFECT: FILTER ROLL ##########################"]
		
		
	
	def _masterRepeat(self, value):
  		if not self._shift_pressed:
  			if self._rack[self._parent.current_track]:
  				self._rack[self._parent.current_track].parameters[5].value = (value * 40)
		else:
			if(value == 1):
				if(self._holdToggle):
					self._holdToggle = False
					self._parent.show_message("########################################################################################## MODE: MOMENTARY ##########################")
					self._newStopAll_button.send_value(0)
				else:
					self._holdToggle = True
					self._parent.show_message("########################################################################################## MODE: HOLD ##########################")
					self._newStopAll_button.send_value(1)
			
				
	def _device_toggle(self, value, sender):
		id = sender.message_identifier() - 82		
		if not self._shift_pressed:		
			if(self._holdToggle):
				if(value == 1):
					if self._repeat_allStateList[self._parent.current_track][id]:
						self._repeat_allStateList[self._parent.current_track][id] = False
						self._amount = 0
					else:
						self._repeat_allStateList[self._parent.current_track] = [False, False, False, False, False]
						self._repeat_allStateList[self._parent.current_track][id] = True
						self._amount = self._paramValues[id]
					self.sceneLight()				
			else:
				self._amount = self._paramValues[id] * value
				self._device_buttons[id].send_value(value)
				
			if self._rack[self._parent.current_track]:
  				self._rack[self._parent.current_track].parameters[self._effectSelect_stateList[self._parent.current_track]].value = self._amount
  				
			
		else:
			if(value == 1):
				self._effectMode_allStateList[self._parent.current_track] = [False, False, False, False, False]
				self._effectMode_allStateList[self._parent.current_track][id] = True
				self.lightEffectMode()
			if(id <= 2):
				self._effectSelect_stateList[self._parent.current_track] = id + 2
			else:
				self._effectSelect_stateList[self._parent.current_track] = id + 3
			self._device_buttons[id].turn_on()
			self._parent.show_message(self._effectMessage[id])
						
		 
		
		
	def sceneLight(self):
		if(self._parent.song().view.selected_track != self._parent.song().master_track):
			if(self._parent._newDjModeToggle_state):
		  		for index in range(len(self._device_buttons)):
		  			if (self._repeat_allStateList[self._parent.current_track][index] == True):
		  				self._device_buttons[index].turn_on()
		  			else:
		  				self._device_buttons[index].turn_off()
  				
  	def lightEffectMode(self):
  		for index in range(len(self._device_buttons)):
  			if (self._effectMode_allStateList[self._parent.current_track][index] == True):
  				self._device_buttons[index].turn_on()
  			else:
  				self._device_buttons[index].turn_off()
  	    		
  		
      

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
		if value:
			self.lightEffectMode()
		else:
			self.sceneLight()
		

				
      
      
      

