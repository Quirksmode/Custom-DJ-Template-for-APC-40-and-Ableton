from _Framework.ButtonElement import ButtonElement #added
from _Framework.EncoderElement import EncoderElement #added
from _Framework.ButtonMatrixElement import ButtonMatrixElement



class ArmToggleComponent():
	'Controls the Arm Button Toggle between modes'
	__module__ = __name__
	
	def __init__(self, parent):
	
		self._parent = parent
		self._arm_buttons = []
		self._shift_button = None
		self._shift_pressed = False
		self._parent.song().view.add_selected_track_listener(self._armLightMode)
		self._parent.current_track = 0
		
		
		self._loop_length = 16
		self._loop_start = 0
		self._clip_length = 0
		self._shift_button = None
		self._current_clip = None
		self._shift_pressed = False
		
		self._beat = 4.0
		self._quant_values = [ self._beat/16.0, self._beat/8.0, self._beat/4, self._beat/2, self._beat, self._beat*2, self._beat*4, self._beat*8 ]
		
		
		## Assign alternate functions to the arm buttons when shift is held down
		self._shiftedFunction = [self._moveLoopLeft32, self._moveLoopRight32, self._moveLoopLeft4, self._moveLoopRight4, self._halveLoop, self._doubleLoop, self._moveLoop, self._toggleLoop]
		
		## Set up the Looper lights
		self._loop_stateList = [False, False, False, False, False, False, False, False]
		self._loop_allStateList = []	    
		for index in range(len(self._loop_stateList)): 
			self._loop_allStateList.append(self._loop_stateList)
			
		## Set up the Utility lights
		self._cueLevel_stateList = [False, True, False, False, False, False, False]
		self._armModeToggle_button = None
		self._armModeToggle_state = False
		
		## Messages
		self._cueMessage = [
		"########################################################################################## CUE MODE ONE: CUE VOLUME // TEMPO ##########################", 
		"########################################################################################## CUE MODE TWO: SCENE SELECT // TEMPO ##############################",
		"########################################################################################## CUE MODE THREE: LOOP SIZE // MOVE LOOP ##############################",
		"########################################################################################## CUE MODE FOUR: MOVE START // MOVE END ##########################",
		"########################################################################################## CUE MODE FIVE: ZOOM CLIP // SCRUB CLIP ##########################"]
		
		
		

			
	def tester(self):
		self._parent.song().view.highlighted_clip_slot.fire()
		
		
	
	def _device_toggle(self, value, sender):
		id = sender.message_channel()
		
		if value == 1:
			if not self._shift_pressed:
				if(self._armModeToggle_state):
					if(id<=4):
						self._parent.transport._cueLevelMode = id+1
						self._cueLevel_stateList = [False, False, False, False, False, False, False]
						self._cueLevel_stateList[id] = True
						self.armLightUtility()
						self._parent.transport._tempo_encoder_control.release_parameter()
						self._parent.show_message(self._cueMessage[id])
					if(id==5):
						self._instant1Bar()
					if(id>=6):
						self._shiftedFunction[id]()
					## Assign Cue Volume (Temporary hack until I get the correct Api Values)
					if(id==0):
						self._parent.transport._tempo_encoder_control.connect_to(self._parent.song().master_track.mixer_device.cue_volume)
				else:
					self.get_current_clip()
					if self._current_clip != None:
						current_clip = self._current_clip
						if not self._shift_pressed:
							if current_clip.looping == 1:
								if self._loop_allStateList[self._parent.current_track][id]:
									self._loop_allStateList[self._parent.current_track][id] = False
									current_clip.loop_end = self._loop_start + 4
									current_clip.looping = 0;
								else:
									self._loop_allStateList[self._parent.current_track] = [False, False, False, False, False, False, False, False]
									self._loop_allStateList[self._parent.current_track][id] = True
									current_clip.loop_end = current_clip.loop_start + self._quant_values[id]
							else:
								self._loop_allStateList[self._parent.current_track] = [False, False, False, False, False, False, False, False]
								self._loop_allStateList[self._parent.current_track][id] = True
								current_clip.looping = 1
								
								self._loop_start = round(current_clip.playing_position / 4.0) * 4
								if (self._loop_start <= current_clip.playing_position):
									self._loop_start = self._loop_start + 4
									
								current_clip.loop_end = self._loop_start + 0.5
								current_clip.loop_start = self._loop_start
								# Twice to fix a weird bug
								current_clip.loop_end = self._loop_start + self._quant_values[id]
								# Thrice to fix an even weirder bug
								current_clip.loop_start = self._loop_start
								current_clip.loop_end = self._loop_start + self._quant_values[id]
								
							self.armLightLoop()
			else: 
				self._shiftedFunction[id]()
	
	
	## Shifted button functions
	def _moveLoopLeft4(self):
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 1
			if current_clip.loop_start >= 4.0:
				current_clip.loop_end = current_clip.loop_end - 4.0
				current_clip.loop_start = current_clip.loop_start - 4.0
			else:
				current_clip.loop_end = 0.0 + self._loop_length
				current_clip.loop_start = 0.0
			if was_playing == 0:
				current_clip.looping = 0
	
	
	def _moveLoopRight4(self):
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 1
			current_clip.loop_end = current_clip.loop_end + 4.0
			current_clip.loop_start = current_clip.loop_start + 4.0
			if was_playing == 0:
				current_clip.looping = 0
	
	
	def _moveLoopLeft32(self):
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 1
			if current_clip.loop_start >= 4.0:
				current_clip.loop_end = current_clip.loop_end - 32.0
				current_clip.loop_start = current_clip.loop_start - 32.0
			else:
				current_clip.loop_end = 0.0 + self._loop_length
				current_clip.loop_start = 0.0
			if was_playing == 0:
				current_clip.looping = 0
	
	
	def _moveLoopRight32(self):
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 1
			current_clip.loop_end = current_clip.loop_end + 32.0
			current_clip.loop_start = current_clip.loop_start + 32.0
			if was_playing == 0:
				current_clip.looping = 0
		
	
	def _halveLoop(self):
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 1
			if self._loop_length <= 128:
				self._loop_length = self._loop_length / 2.0
			else:
				self._loop_length = self._loop_length - 16 
			current_clip.loop_end = current_clip.loop_start + self._loop_length
			if was_playing == 0:
				current_clip.looping = 0
	
	
	def _doubleLoop(self):
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 1
			if self._loop_length <= 128:
				self._loop_length = self._loop_length * 2.0
			else:
				self._loop_length = self._loop_length + 16 
			current_clip.loop_end = current_clip.loop_start + self._loop_length
			if was_playing == 0:
				current_clip.looping = 0
	
	
	def _moveLoop(self):
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 1
			self._loop_length = current_clip.loop_end - current_clip.loop_start
			self._loop_start = round(current_clip.playing_position / 4.0) * 4
			current_clip.loop_end = self._loop_start + self._loop_length
			current_clip.loop_start = self._loop_start
			current_clip.loop_end = self._loop_start + self._loop_length
			if was_playing == 0:
				current_clip.looping = 0
	
	
	def _toggleLoop(self):
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			was_playing = current_clip.looping
			if current_clip.looping == 1:
				current_clip.looping = 0
				self._arm_buttons[7].turn_off()
			else:
				self._clip_length = current_clip.length
				current_clip.looping = 1
				self._arm_buttons[7].turn_on()
	
				
	def _instant1Bar(self):
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 1
			self._arm_buttons[7].turn_on()
			self._loop_length = current_clip.loop_end - current_clip.loop_start
			self._loop_start = round(current_clip.playing_position / 4.0) * 4
			current_clip.loop_end = self._loop_start + 4
			current_clip.loop_start = self._loop_start
			current_clip.loop_end = self._loop_start + 4
		
						
	def _toggleArmMode(self, value):
		if value == 1:
			if(self._armModeToggle_state):
				self._newDetailView_button.turn_off()
				self._armModeToggle_state = False
				self.armLightLoop()
				self._parent.show_message("########################################################################################## LOOP MODE ##############################")
			else:
				self._newDetailView_button.turn_on()
				self._armModeToggle_state = True
				self.armLightUtility()
				self._parent.show_message("########################################################################################## UTILITY MODE ##############################")
				
				
	def _armLightMode(self):
		if(self._parent._newDjModeToggle_state):
			if(self._armModeToggle_state):
				self.armLightUtility()
			else:
				self.armLightLoop()
	
	
	def armLightLoop(self):
		if(self._parent.song().view.selected_track != self._parent.song().master_track):
			for index in range(len(self._arm_buttons)):
				if (self._loop_allStateList[self._parent.current_track][index] == True):
					self._arm_buttons[index].turn_on()
				else:
					self._arm_buttons[index].turn_off()
				
	
	def armLightUtility(self):
		for index in range(len(self._cueLevel_stateList)):
			if (self._cueLevel_stateList[index] == True):
				self._arm_buttons[index].turn_on()
			else:
				self._arm_buttons[index].turn_off()
		self.get_current_clip()
		if self._current_clip != None:
			current_clip = self._current_clip
			if current_clip.looping == 1:
				self._arm_buttons[7].turn_on()
			else:
				self._arm_buttons[7].turn_off()
		else:
			self._arm_buttons[7].turn_off()
			

				 

	def get_current_clip(self):
		if (self._parent.song().view.highlighted_clip_slot != None):
			clip_slot = self._parent.song().view.highlighted_clip_slot
			if clip_slot.has_clip:
				self._current_clip = clip_slot.clip
			else:
				self._current_clip = None
		else:
			self._current_clip = None
	
	
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
		
	
	