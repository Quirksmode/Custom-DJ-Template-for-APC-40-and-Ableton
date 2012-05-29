import Live
from _Framework.TransportComponent import TransportComponent
from _Framework.ButtonElement import ButtonElement #added
from _Framework.EncoderElement import EncoderElement #added
from _Framework.ButtonMatrixElement import ButtonMatrixElement



class TrackControlComponent(TransportComponent):
	'Applies Rack to Track Control'
	__module__ = __name__
	
	def __init__(self, parent):
		TransportComponent.__init__(self)
		self._parent = parent
		self._parent.song().view.add_selected_track_listener(self.get_current_track)
		self.current_track = 0
		self._trackEncoders = []
		self.newTrackEncoder_encoder = None
		self.newDeviceEncoder_encoder = None
		self._tempo_encoder_control = None #added
		self.savedValueToggle = False
		
	def get_current_track(self):	
		track_index = 0
		for track in self._parent.song().tracks:
			if track == self._parent.song().view.selected_track:
				break
			track_index += 1
		self.current_track = track_index
		
		if(self._parent.song().view.selected_track != self._parent.song().master_track):
			for parameter in range(8):
				self._trackEncoders[parameter].connect_to(self._parent.song().tracks[self.current_track].devices[1].parameters[parameter+1])	
				
			
		

