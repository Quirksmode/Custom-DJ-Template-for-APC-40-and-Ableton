
import Live
from _Framework.TransportComponent import TransportComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement #added
class ShiftableTransportComponent(TransportComponent):
	__doc__ = ' TransportComponent that only uses certain buttons if a shift button is pressed '

	def __init__(self, parent):
		TransportComponent.__init__(self)
		self._parent = parent
		self._shift_button = None
		self._quant_toggle_button = None
		self._shift_pressed = False
		self._last_quant_value = Live.Song.RecordingQuantization.rec_q_eight
		self.song().add_midi_recording_quantization_listener(self._on_quantisation_changed)
		self._on_quantisation_changed()
		#added
		self._undo_button = None #added from OpenLabs SpecialTransportComponent script
		self._redo_button = None #added from OpenLabs SpecialTransportComponent script
		self._bts_button = None #added from OpenLabs SpecialTransportComponent script
		self._cueLevelMode = 1
		self._tempo_encoder_control = None
		self._moveLoop = 0
		self._scrollRedBox = 0
		self._z = 4
		self._counter = 0
		self._beat = 4.0
		self._quant_values = [self._beat/16.0, self._beat/8.0, self._beat/4, self._beat/2, self._beat, self._beat*2, self._beat*4, self._beat*8 ]
		


	def disconnect(self):
		TransportComponent.disconnect(self)
		if self._shift_button != None:
			self._shift_button.remove_value_listener(self._shift_value)
			self._shift_button = None
		if self._quant_toggle_button != None:
			self._quant_toggle_button.remove_value_listener(self._quant_toggle_value)
			self._quant_toggle_button = None
		self.song().remove_midi_recording_quantization_listener(self._on_quantisation_changed)
		
	
	
	def set_tempo_encoder(self, control):
		assert ((control == None) or (isinstance(control, EncoderElement) and (control.message_map_mode() is Live.MidiMap.MapMode.relative_two_compliment)))
		if (self._tempo_encoder_control != None):
		    self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
		self._tempo_encoder_control = control
		if (self._tempo_encoder_control != None):
		    self._tempo_encoder_control.add_value_listener(self._tempo_encoder_value)
		self.update()



	def set_shift_button(self, button):
		assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
		if self._shift_button != button:
			if self._shift_button != None:
				self._shift_button.remove_value_listener(self._shift_value)
			self._shift_button = button
			if self._shift_button != None:
				self._shift_button.add_value_listener(self._shift_value)
			##self._rebuild_callback()
			self.update()


	def set_quant_toggle_button(self, button):
		assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
		if self._quant_toggle_button != button:
			if self._quant_toggle_button != None:
				self._quant_toggle_button.remove_value_listener(self._quant_toggle_value)
			self._quant_toggle_button = button
			if self._quant_toggle_button != None:
				self._quant_toggle_button.add_value_listener(self._quant_toggle_value)
			##self._rebuild_callback()
			self.update()


	def update(self):
		self._on_metronome_changed()
		self._on_overdub_changed()
		self._on_quantisation_changed()


	def _shift_value(self, value):
		assert (self._shift_button != None)
		assert (value in range(128))
		self._shift_pressed = value != 0
		if self.is_enabled():
			self.update()


	def _metronome_value(self, value):
		if not self._shift_pressed:
			TransportComponent._metronome_value(self, value)


	def _overdub_value(self, value):
		if not self._shift_pressed:
			TransportComponent._overdub_value(self, value)


	def _quant_toggle_value(self, value):
		assert (self._quant_toggle_button != None)
		assert (value in range(128))
		assert (self._last_quant_value != Live.Song.RecordingQuantization.rec_q_no_q)
		if (self.is_enabled() and (not self._shift_pressed)):
			if ((value != 0) or (not self._quant_toggle_button.is_momentary())):
				quant_value = self.song().midi_recording_quantization
				if (quant_value != Live.Song.RecordingQuantization.rec_q_no_q):
					self._last_quant_value = quant_value
					self.song().midi_recording_quantization = Live.Song.RecordingQuantization.rec_q_no_q
				else:
					self.song().midi_recording_quantization = self._last_quant_value


	def _on_metronome_changed(self):
		if not self._shift_pressed:
			TransportComponent._on_metronome_changed(self)


	def _on_overdub_changed(self):
		if not self._shift_pressed:
			TransportComponent._on_overdub_changed(self)


	def _on_quantisation_changed(self):
		if self.is_enabled():
			quant_value = self.song().midi_recording_quantization
			quant_on = (quant_value != Live.Song.RecordingQuantization.rec_q_no_q)
			if quant_on:
				self._last_quant_value = quant_value
			if ((not self._shift_pressed) and (self._quant_toggle_button != None)):
				if quant_on:
					self._quant_toggle_button.turn_on()
				else:
					self._quant_toggle_button.turn_off()


	""" from OpenLabs module SpecialTransportComponent """
	
	def set_undo_button(self, undo_button):
	    assert isinstance(undo_button, (ButtonElement,
	                                    type(None)))
	    if (undo_button != self._undo_button):
	        if (self._undo_button != None):
	            self._undo_button.remove_value_listener(self._undo_value)
	        self._undo_button = undo_button
	        if (self._undo_button != None):
	            self._undo_button.add_value_listener(self._undo_value)
	        self.update()
	
	
	
	def set_redo_button(self, redo_button):
	    assert isinstance(redo_button, (ButtonElement,
	                                    type(None)))
	    if (redo_button != self._redo_button):
	        if (self._redo_button != None):
	            self._redo_button.remove_value_listener(self._redo_value)
	        self._redo_button = redo_button
	        if (self._redo_button != None):
	            self._redo_button.add_value_listener(self._redo_value)
	        self.update()
	
	
	def _undo_value(self, value):
	    if self._shift_pressed: #added
	        assert (self._undo_button != None)
	        assert (value in range(128))
	        if self.is_enabled():
	            if ((value != 0) or (not self._undo_button.is_momentary())):
	                if self.song().can_undo:
	                    self.song().undo()
	
	
	def _redo_value(self, value):
		if self._shift_pressed: #added
			assert (self._redo_button != None)
			assert (value in range(128))
			if self.is_enabled():
				if ((value != 0) or (not self._redo_button.is_momentary())):
					if self.song().can_redo:
						self.song().redo()
	
	def _tempo_encoder_value(self, value):
		if(self._cueLevelMode == 1):
			if not self._shift_pressed:
				## Change Cue Volume
				backwards = (value >= 64)
			else:
				## Change Tempo
				assert (self._tempo_encoder_control != None)
				assert (value in range(128))
				backwards = (value >= 64)
				step = 0.1 #step = 1.0 #reduce this for finer control; 1.0 is 1 bpm
				if backwards:
				    amount = (value - 128)
				  
				else:
				    amount = value
				  
				tempo = max(20, min(999, (self.song().tempo + (amount * step))))
				self.song().tempo = tempo
				
		if(self._cueLevelMode == 2):
			if not self._shift_pressed:
				## Move Red View Box
				backwards = (value >= 64)
				if backwards:
					if (self._scrollRedBox >= 5):
						self._scrollRedBox -= 1
					else:
						self._scrollRedBox = 0
				else:
					self._scrollRedBox += 1
				self._parent._session.set_offsets(0, self._scrollRedBox)
				self._parent._session.update()
			else:
				## Change Tempo
				assert (self._tempo_encoder_control != None)
				assert (value in range(128))
				backwards = (value >= 64)
				step = 0.1 #step = 1.0 #reduce this for finer control; 1.0 is 1 bpm
				if backwards:
				    amount = (value - 128)				  
				else:
				    amount = value				  
				tempo = max(20, min(999, (self.song().tempo + (amount * step))))
				self.song().tempo = tempo
		
		elif(self._cueLevelMode == 3):
			self.get_current_clip()
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 1
			

			if not self._shift_pressed:
				## Change Loop Length
				backwards = (value >= 64)
				if backwards:
					self._counter+=0.2
					if (self._counter >= 1):
						self._counter = 0
						if (self._z > 0):
							self._z -= 1
							self._parent.song().view.highlighted_clip_slot.clip.loop_end = self._parent.song().view.highlighted_clip_slot.clip.loop_start + self._quant_values[self._z]
				else:
					self._counter+=0.2
					if (self._counter >= 1):
						self._counter = 0
						if (self._z < (len(self._quant_values))-1):
							self._z += 1
							self._parent.song().view.highlighted_clip_slot.clip.loop_end = self._parent.song().view.highlighted_clip_slot.clip.loop_start + self._quant_values[self._z]
			else:
				## Change Loop Position
				backwards = (value >= 64)
				if backwards:
					self._moveLoop = -4
				else:
					self._moveLoop = 4
				self._parent.song().view.highlighted_clip_slot.clip.loop_end += self._moveLoop
				self._parent.song().view.highlighted_clip_slot.clip.loop_start += self._moveLoop

			if was_playing == 0:
				current_clip.looping = 0
				
		elif(self._cueLevelMode == 4):
			self.get_current_clip()
			current_clip = self._current_clip
			was_playing = current_clip.looping
			current_clip.looping = 0
			

			if not self._shift_pressed:
				## Change Loop Position
				backwards = (value >= 64)
				if backwards:
					self._moveLoop = -4
				else:
					self._moveLoop = 4
				self._parent.song().view.highlighted_clip_slot.clip.loop_start += self._moveLoop
			else:
				## Change Loop Position
				backwards = (value >= 64)
				if backwards:
					self._moveLoop = -4
				else:
					self._moveLoop = 4
				self._parent.song().view.highlighted_clip_slot.clip.loop_end += self._moveLoop

			if was_playing == 1:
				current_clip.looping = 1
				
		elif(self._cueLevelMode == 5):
				
			if not self._shift_pressed:
				## Zoomer will go here
				backwards = (value >= 64)		
			else:
				## Scrub Playing Position
				backwards = (value >= 64)
				if backwards:
				  self._y = -32
				else:
				  self._y = 32
				self._parent.song().view.highlighted_clip_slot.clip.move_playing_pos(self._y)
				
			
			
	def get_current_clip(self):
		if (self._parent.song().view.highlighted_clip_slot != None):
			clip_slot = self._parent.song().view.highlighted_clip_slot
			if clip_slot.has_clip:
				self._current_clip = clip_slot.clip
			else:
				self._current_clip = None
		else:
			self._current_clip = None
