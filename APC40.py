
import Live
from APC import APC
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.MixerComponent import MixerComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.ChannelTranslationSelector import ChannelTranslationSelector
from EncModeSelectorComponent import EncModeSelectorComponent
from RingedEncoderElement import RingedEncoderElement
from DetailViewCntrlComponent import DetailViewCntrlComponent
from ShiftableDeviceComponent import ShiftableDeviceComponent
from ShiftableTransportComponent import ShiftableTransportComponent
from ShiftTranslatorComponent import ShiftTranslatorComponent
from PedaledSessionComponent import PedaledSessionComponent
from SpecialMixerComponent import SpecialMixerComponent


from SpecialChanStripComponent import SpecialChanStripComponent
from _Framework.DeviceComponent import DeviceComponent 

# Quirksmode Custom Imports
from SceneEffectComponent import SceneEffectComponent
from ResetComponent import ResetComponent
from ArmToggleComponent import ArmToggleComponent
from TrackControlComponent import TrackControlComponent



class APC40(APC):
    __doc__ = " Script for Akai's APC40 Controller "
    
    def __init__(self, c_instance):
        APC.__init__(self, c_instance)
        self._device_selection_follows_track_selection = True
        
    def _setup_session_control(self):
    	is_momentary = True
        self._shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 98)        
        right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 96)
        left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 97)
        up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 94)
        down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 95)
        right_button.name = 'Bank_Select_Right_Button'
        left_button.name = 'Bank_Select_Left_Button'
        up_button.name = 'Bank_Select_Up_Button'
        down_button.name = 'Bank_Select_Down_Button'
        self._session = PedaledSessionComponent(8, 5)
        self._session.name = 'Session_Control'
        self._session.set_track_bank_buttons(right_button, left_button)
        self._session.set_scene_bank_buttons(down_button, up_button)
        matrix = ButtonMatrixElement()
        matrix.name = 'Button_Matrix'
        self.scene_launch_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, (index + 82)) for index in range(5) ]
        track_stop_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, index, 52) for index in range(8) ]
        for index in range(len(self.scene_launch_buttons)):
            self.scene_launch_buttons[index].name = 'Scene_'+ str(index) + '_Launch_Button'
        for index in range(len(track_stop_buttons)):
            track_stop_buttons[index].name = 'Track_' + str(index) + '_Stop_Button'
        self.stop_all_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 81)
        self.stop_all_button.name = 'Stop_All_Clips_Button'
        self._session.set_stop_all_clips_button(self.stop_all_button)
        self._session.set_stop_track_clip_buttons(tuple(track_stop_buttons))
        self._session.set_stop_track_clip_value(2)
        
        ## Quirksmode
        self.newZoom_buttons = []
        
        for scene_index in range(5):
            scene = self._session.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            button_row = []

            scene.set_launch_button(self.scene_launch_buttons[scene_index])
            scene.set_triggered_value(2)
            for track_index in range(8):
                button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track_index, (scene_index + 53))
                
                ## Quirksmode - This moves the zoomer to allow for scene launch customisation (Currently not working 100%)
                if(track_index == 4):
                	self.newZoom_buttons.append(button)
                
                button.name = str(track_index) + '_Clip_' + str(scene_index) + '_Button'
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index)
                clip_slot.set_triggered_to_play_value(2)
                clip_slot.set_triggered_to_record_value(4)
                clip_slot.set_stopped_value(3)
                clip_slot.set_started_value(1)
                clip_slot.set_recording_value(3)
                clip_slot.set_launch_button(button)

            matrix.add_row(tuple(button_row))

        self._session.set_slot_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 67))
        self._session.selected_scene().name = 'Selected_Scene'
        self._session.selected_scene().set_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 64))
        self._session_zoom = SessionZoomingComponent(self._session)
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_button_matrix(matrix)
        self._session_zoom.set_zoom_button(self._shift_button)
        self._session_zoom.set_nav_buttons(up_button, down_button, left_button, right_button)
        self._session_zoom.set_scene_bank_buttons(tuple(self.newZoom_buttons))
        self._session_zoom.set_stopped_value(3)
        self._session_zoom.set_selected_value(5)
        return None #return session

    def _setup_mixer_control(self):
        is_momentary = True
        
        ## Quirksmode
        self.arm_buttons = []
        
        self._mixer = SpecialMixerComponent(self, 8) #added self for parent
        self._mixer.name = 'Mixer'
        self._mixer.master_strip().name = 'Master_Channel_Strip'
        self._mixer.selected_strip().name = 'Selected_Channel_Strip'
        for track in range(8):
            self.strip = self._mixer.channel_strip(track)
            self.strip.name = 'Channel_Strip_' + str(track)
            volume_control = SliderElement(MIDI_CC_TYPE, track, 7)
            arm_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 48)
            solo_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 49)
            mute_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 50)
            select_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 51)
            volume_control.name = str(track) + '_Volume_Control'
            arm_button.name = str(track) + '_Arm_Button'
            solo_button.name = str(track) + '_Solo_Button'
            mute_button.name = str(track) + '_Mute_Button'
            select_button.name = str(track) + '_Select_Button'
            self.strip.set_volume_control(volume_control)
            
            ##Quirksmode
            self.arm_buttons.append(arm_button)
            
            self.strip.set_arm_button(arm_button)
            self.strip.set_solo_button(solo_button)
            self.strip.set_mute_button(mute_button)
            self.strip.set_select_button(select_button)
            self.strip.set_shift_button(self._shift_button)
            self.strip.set_invert_mute_feedback(True)
        crossfader = SliderElement(MIDI_CC_TYPE, 0, 15)
        
        
        master_volume_control = SliderElement(MIDI_CC_TYPE, 0, 14)
        master_select_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 80)
        ##self._prehear_control = EncoderElement(MIDI_CC_TYPE, 0, 47, Live.MidiMap.MapMode.relative_two_compliment)
        crossfader.name = 'Crossfader'
        master_volume_control.name = 'Master_Volume_Control'
        master_select_button.name = 'Master_Select_Button'
        ##self._prehear_control.name = 'Prehear_Volume_Control'
        self._mixer.set_crossfader_control(crossfader)
        ##self._mixer.set_prehear_volume_control(self._prehear_control)
        self._mixer.master_strip().set_volume_control(master_volume_control)
        self._mixer.master_strip().set_select_button(master_select_button)

    def _setup_custom_components(self):
        self._setup_device_and_transport_control()
        self._setup_global_control()
        self._setup_djModeToggle()
        
        
    
    def _setup_djModeToggle(self):
    	self._newDjModeToggle_state = False
    	
    	## How many tracks?
    	self._trackTotal = len(self.song().tracks)
    
    	## Re-Assign Metronome to Dj Mode toggle
        self._newDjModeToggle_button = self.transport._metronome_button
        self.transport.set_metronome_button(None)
        self._newDjModeToggle_button.add_value_listener(self._toggleDjMode)
        
        ## Assign Cue Volume (Temporary hack until I get the correct Api Values)
        self.transport._tempo_encoder_control.connect_to(self.song().master_track.mixer_device.cue_volume)
        
        
        	
    def _toggleDjMode(self, value):
    	if value == 1:
			if(self._newDjModeToggle_state):
				self._newDjModeToggle_button.turn_off()
				self._newDjModeToggle_state = False
				self.show_message("########################################################################################## DJ MODE: OFF ##############################")
				self._disconnect_djMode()
				self.transport._cueLevelMode = 1
				self.device_bank_buttons[4].turn_on()
				self.transport._tempo_encoder_control.connect_to(self.song().master_track.mixer_device.cue_volume)
				
				
				
				
			else:
				self._newDjModeToggle_button.turn_on()
				self._newDjModeToggle_state = True
				self.show_message("########################################################################################## DJ MODE: ON ##############################")
				self._setup_djMode()
				self.transport._cueLevelMode = 2
				self.device_bank_buttons[4].turn_off()
				self.transport._tempo_encoder_control.release_parameter()
				
				
				
    
	
				
    def _setup_djMode(self):
    	## Assign imports
        self.sceneEffect = SceneEffectComponent(self)
        self.reset = ResetComponent(self)
        self.armmode = ArmToggleComponent(self)
        self.trackControl = TrackControlComponent(self)
    
    	is_momentary = True
    	
    	       
        ##### Scene Effect Component
        self.sceneEffect.set_shift_button(self._shift_button)
        
        for scene_index in range(5):
        	self.sceneEffect.newScene_button = self._session.scene(scene_index)._launch_button
        	self._session.scene(scene_index).set_launch_button(None)
        	self.sceneEffect.newScene_button.add_value_listener(self.sceneEffect._device_toggle, True)
        	self.sceneEffect._device_buttons.append(self.sceneEffect.newScene_button)
        
        # Re-assign the stop all clips button
        self.sceneEffect._newStopAll_button = self._session._stop_all_button
        self._session.set_stop_all_clips_button(None)
        self.sceneEffect._newStopAll_button.add_value_listener(self.sceneEffect._masterRepeat)
        
        
          
        ##### Reset Component
        self.reset.set_shift_button(self._shift_button)
        
        #Re-assign Play and Stop buttons to Reset Track and All
        self.reset.reset_button = self.transport._play_button
        self.transport.set_play_button(None)
        self.reset.reset_button.add_value_listener(self.reset.reset_track)
        
        self.reset.resetAll_button = self.transport._stop_button
        self.transport.set_stop_button(None)
        self.reset.resetAll_button.add_value_listener(self.reset.reset_all)
        
        
        	
        ##### Arm Toggle Component
        self.armmode.set_shift_button(self._shift_button)
        
        # Re-Assign Clip/Track Button to Loop/Utility toggle
        self.armmode._newDetailView_button = self.detail_view_toggler._detail_toggle_button
        self.detail_view_toggler.set_detail_toggle_button(None)
        self.armmode._newDetailView_button.add_value_listener(self.armmode._toggleArmMode)
        
        
        
        # Re-assign Arm button functionality
        for track in range(8):
        	self.armmode.newArm_button = self._mixer.channel_strip(track)._arm_button
        	self._mixer.channel_strip(track).set_arm_button(None)
        	self.armmode.newArm_button.add_value_listener(self.armmode._device_toggle, True)
        	self.armmode._arm_buttons.append(self.armmode.newArm_button)
        
        
        ##### Re-assign Track Control Ringed Encoders
        self.trackControl._trackEncoders = []
        for encoder_index in range(8):
        	self.newTrackEncoder_encoder = self.global_param_controls[encoder_index]
        	self.encoder_modes.set_controls(None)
        	self.trackControl._trackEncoders.append(self.newTrackEncoder_encoder)
        
        
        self.get_current_track()	
        if(self.song().view.selected_track != self.song().master_track):
        	for device in self.song().tracks[self.current_track].devices:
				if device.name == "DJ EQ and FX":
					for parameter in range(8):
						self.trackControl._trackEncoders[parameter].connect_to(device.parameters[parameter+1])
						
	
	    
    def _disconnect_djMode(self):
    
    	##### Disconnect Scene Effect Component    	
    	# Re-assign the Scene Start Buttons
    	for scene_index in range(5):
        	self.sceneEffect._device_buttons[scene_index].remove_value_listener(self.sceneEffect._device_toggle)
        	self._session.scene(scene_index).set_launch_button(self.scene_launch_buttons[scene_index])
        self.sceneEffect._device_buttons = []
    	# Re-assign the stop all clips button
    	self.sceneEffect._newStopAll_button.remove_value_listener(self.sceneEffect._masterRepeat)
    	self.sceneEffect._newStopAll_button = None
    	self._session.set_stop_all_clips_button(self.stop_all_button)    	        
        self.song().view.remove_selected_track_listener(self.sceneEffect.sceneLight)
        

          
        ##### Disconnect Reset Component       
        # Re-assign the Play Button
        self.reset.reset_button.remove_value_listener(self.reset.reset_track)
        self.reset.reset_button = None
        self.transport.set_play_button(self.play_button)
        # Re-assign the Stop Button
        self.reset.resetAll_button.remove_value_listener(self.reset.reset_all)
        self.reset.resetAll_button = None
        self.transport.set_stop_button(self.stop_button)
        
        
      
        ##### Disconnect Arm Toggle Component
    	for track in range(8):
        	self.armmode._arm_buttons[track].remove_value_listener(self.armmode._device_toggle)
        	self._mixer.channel_strip(track).set_arm_button(self.arm_buttons[track])
        self.armmode._arm_buttons = []
        
        self.armmode._newDetailView_button.remove_value_listener(self.armmode._toggleArmMode)
    	self.armmode._newDetailView_button = None
        self.detail_view_toggler.set_detail_toggle_button(self.device_bank_buttons[4])
        self.song().view.remove_selected_track_listener(self.armmode._armLightMode)
        
        
        
        ##### Disconnect Track Control Ringed Encoders
        self.trackControl._trackEncoders = []
        self.song().view.remove_selected_track_listener(self.trackControl.get_current_track)
        
	
	##### Link the cutoffs for the Scene Effect Parameters
    def _linkCutoff(self, value):
    	for device in self.song().tracks[self.current_track].devices:
				if device.name == "Scene Launch Effects":
					device.parameters[1].value = value
						
    
    def _setup_device_and_transport_control(self):
        is_momentary = True
        self.device_bank_buttons = []
        self.device_param_controls = []
        bank_button_labels = ('Clip_Track_Button', 'Device_On_Off_Button', 'Previous_Device_Button', 'Next_Device_Button', 'Detail_View_Button', 'Rec_Quantization_Button', 'Midi_Overdub_Button', 'Metronome_Button')
        for index in range(8):
            self.device_bank_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 58 + index))
            self.device_bank_buttons[-1].name = bank_button_labels[index]
            ring_mode_button = ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 24 + index)
            ringed_encoder = RingedEncoderElement(MIDI_CC_TYPE, 0, 16 + index, Live.MidiMap.MapMode.absolute)
            ringed_encoder.set_ring_mode_button(ring_mode_button)
            ringed_encoder.name = 'Device_Control_' + str(index)
            ring_mode_button.name = ringed_encoder.name + '_Ring_Mode_Button'
            
            ## Quirksmode
            ##### Link the cutoffs for the Scene Effect Parameters
            if (index == 0):
            	ringed_encoder.add_value_listener(self._linkCutoff)
            
            self.device_param_controls.append(ringed_encoder)
        self.device = ShiftableDeviceComponent()
        self.device.name = 'Device_Component'
        self.device.set_bank_buttons(tuple(self.device_bank_buttons))
        self.device.set_shift_button(self._shift_button)
        self.device.set_parameter_controls(tuple(self.device_param_controls))
        self.device.set_on_off_button(self.device_bank_buttons[1])
        self.set_device_component(self.device)
        self.detail_view_toggler = DetailViewCntrlComponent()
        self.detail_view_toggler.name = 'Detail_View_Control'
        self.detail_view_toggler.set_shift_button(self._shift_button)
        self.detail_view_toggler.set_device_clip_toggle_button(self.device_bank_buttons[0])
        self.detail_view_toggler.set_detail_toggle_button(self.device_bank_buttons[4])
        self.detail_view_toggler.set_device_nav_buttons(self.device_bank_buttons[2], self.device_bank_buttons[3])
        self.transport = ShiftableTransportComponent(self) ## Quirksmode added self
        self.transport.name = 'Transport'
        self.play_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 91)
        self.play_button.name = 'Play_Button'
        
        self.stop_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 92)
        self.record_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 93)
        nudge_up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 100)
        nudge_down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 101)
        tap_tempo_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 99)
        self.stop_button.name = 'Stop_Button'
        self.record_button.name = 'Record_Button'
        nudge_up_button.name = 'Nudge_Up_Button'
        nudge_down_button.name = 'Nudge_Down_Button'
        tap_tempo_button.name = 'Tap_Tempo_Button'
        self.transport.set_shift_button(self._shift_button)
        self.transport.set_play_button(self.play_button)
        self.transport.set_stop_button(self.stop_button)
        self.transport.set_record_button(self.record_button)
        self.transport.set_nudge_buttons(nudge_up_button, nudge_down_button)
        self.transport.set_undo_button(nudge_down_button) #shifted nudge
        self.transport.set_redo_button(nudge_up_button) #shifted nudge
        self.transport.set_tap_tempo_button(tap_tempo_button)
        self.transport.set_quant_toggle_button(self.device_bank_buttons[5])
        self.transport.set_overdub_button(self.device_bank_buttons[6])
        self.transport.set_metronome_button(self.device_bank_buttons[7])
        self._prehear_control = EncoderElement(MIDI_CC_TYPE, 0, 47, Live.MidiMap.MapMode.relative_two_compliment)
        self.transport.set_tempo_encoder(self._prehear_control) #shifted prehear
        bank_button_translator = ShiftTranslatorComponent()
        bank_button_translator.set_controls_to_translate(tuple(self.device_bank_buttons))
        bank_button_translator.set_shift_button(self._shift_button)

    def _setup_global_control(self):
        is_momentary = True
        global_bank_buttons = []
        self.global_param_controls = []
        for index in range(8):
            ring_button = ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 56 + index)
            ringed_encoder = RingedEncoderElement(MIDI_CC_TYPE, 0, 48 + index, Live.MidiMap.MapMode.absolute)
            ringed_encoder.name = 'Track_Control_' + str(index)
            ring_button.name = ringed_encoder.name + '_Ring_Mode_Button'
            ringed_encoder.set_ring_mode_button(ring_button)
            self.global_param_controls.append(ringed_encoder)
        global_bank_buttons = []
        global_bank_labels = ('Pan_Button', 'Send_A_Button', 'Send_B_Button', 'Send_C_Button')
        for index in range(4):
            global_bank_buttons.append(ButtonElement(not is_momentary, MIDI_NOTE_TYPE, 0, 87 + index))
            global_bank_buttons[-1].name = global_bank_labels[index]
        self.encoder_modes = EncModeSelectorComponent(self._mixer)
        self.encoder_modes.name = 'Track_Control_Modes'
        self.encoder_modes.set_modes_buttons(global_bank_buttons)
        self.encoder_modes.set_controls(tuple(self.global_param_controls))
        self.global_translation_selector = ChannelTranslationSelector()
        self.global_translation_selector.name = 'Global_Translations'
        self.global_translation_selector.set_controls_to_translate(tuple(self.global_param_controls))
        self.global_translation_selector.set_mode_buttons(tuple(global_bank_buttons))

    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        
        ## Quirksmode
        if(self._newDjModeToggle_state):
        
	    	if self.application().view.is_view_visible('Detail/Clip'):
	    		self.application().view.show_view('Detail/DeviceChain')
	    		self.application().view.is_view_visible('Detail/DeviceChain')
	    	else:
	    		self.application().view.show_view('Detail/Clip')
	    		self.application().view.is_view_visible('Detail/Clip')
		
	    	if(self.song().view.selected_track != self.song().master_track):
		    	if (self.song().view.selected_track.playing_slot_index > -1):
		            self.song().view.selected_scene = self.song().scenes[self.song().view.selected_track.playing_slot_index]
	    
        
	        track_index = 0
	        for track in self.song().tracks:
	        	if track == self.song().view.selected_track:
	        		break
	        	track_index += 1
	        self.current_track = track_index
            
        
        
        track = self.song().view.selected_track
        device_to_select = track.view.selected_device
        if device_to_select == None and len(track.devices) > 0:
            device_to_select = track.devices[0]
        if device_to_select != None:
            self.song().view.select_device(device_to_select)
        self._device_component.set_device(device_to_select)
        return None
    
    
    
    
    
    ######################### Utils
    
    # Get the current track    
    def get_current_track(self):
    	track_index = 0
    	for track in self.song().tracks:
    		if track == self.song().view.selected_track:
    			break
    		track_index += 1
    	self.current_track = track_index
    
    
    # Get the device on the given track by the given name.
    def GetDeviceByName(self, trackIndex, deviceName):
        for device in self.song().tracks[trackIndex].devices:
            if (device.name == deviceName):
                return device
        return None

    # Get the value of the given device in the given track by the given parameter name. 
    def GetDeviceParameter(self, device, paramName):
        for deviceParam in device.parameters:
            if (deviceParam.name == paramName):
                return deviceParam.value
            return None

    # Set the given parameter name of the given device to the given value.
    def SetDeviceParameter(self, device, paramName, value):
        for deviceParam in device.parameters:
            if (deviceParam.name == paramName):
                deviceParam.value = value
                pass

    # Toggles the given param of the given device. Usefull for on/off effects, etc.
    def ToggleDeviceParameter(self, device, paramName):
        for deviceParam in device.parameters:
            if (deviceParam.name == paramName):
                if (deviceParam.value == 1):
                    deviceParam.value = 0
                else:
                    deviceParam.value = 1
                pass

    # Returns if the given track has a triggered clip.
    def TrackHasTriggeredClip(self, track):
        for clipSlot in track.clip_slots:
            if (clipSlot.has_clip):
                if (clipSlot.clip.is_triggered):
                    return True
        return False

    # Returns if the given track has a playing clip.
    def TrackHasPlayingClip(self, track):
        for clipSlot in track.clip_slots:
            if (clipSlot.has_clip):
                if (clipSlot.clip.is_playing):
                    return True
        return False

    
    def _product_model_id_byte(self):
        return 115
        
        
        
    
        
        
        


