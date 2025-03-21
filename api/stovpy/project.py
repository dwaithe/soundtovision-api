class SToVProject:
    def __init__(self, document_colour='#000000', page=[960,540], duration=300):
        self.document_colour = document_colour
        self.page = page
        self.bpm = 120
        self.sample_rate = 44100
        self.fft_size = 512
        self.time_sig = 1
        self.snap_active = False
        self.snap_offset = 0
        self.num_of_rows = 6
        self.duration = duration
        self.page.append(duration)

        self.sig_reg = []
        self.sig_reg.append([0,None,None,1,4./60,0,'Sin Example',0, self.duration])
        self.sig_reg.append([1,None,None,1,1./60,0,'Square Example',0, self.duration])
        self.sig_reg.append([2,None,None,1,8./60,0,'Triangle Example',0, self.duration])
        self.sig_reg.append([3,None,None,1,8./60,0,'Sawtooth Example',0, self.duration])
        
        
    @property
    def bpm(self):
        return self._bpm
    @bpm.setter
    def bpm(self, value):
        self._bpm = int(value)
    @property
    def time_sig(self):
        return self._time_sig
    @time_sig.setter
    def time_sig(self, value):
        self._time_sig = int(value)
    @property
    def snap_active(self):
        return self._snap_active
    @snap_active.setter
    def snap_active(self, value):
        self._snap_active = bool(value)
    @property
    def snap_offset(self):
        return self._snap_offset
    @snap_offset.setter
    def snap_offset(self, value):
        self._snap_offset = int(value)
    @property
    def num_of_rows(self):
        return self._num_of_rows
    @num_of_rows.setter
    def num_of_rows(self, value):
        self._num_of_rows = int(value)
    #SToVLoop "njqna":["loop",{"type":"loop","lstart":82.1875,"lend":121.1875,"count":5,"remain":5,"midi_PC":null}]}
    
    def rtn_json(self):
        proj_json = {}
        document_settings = {}
        document_settings["document_colour"] = self.document_colour
        document_settings["page"] = self.page
        document_settings["bpm"] = self.bpm
        document_settings["time_sig"] = self.time_sig
        document_settings["snap_active"] = self.snap_active
        document_settings["snap_offset"] = self.snap_offset
        document_settings["num_of_rows"] = self.num_of_rows

        proj_json['document_settings'] = document_settings
        
        proj_json['sig_reg']  = self.sig_reg

        proj_json['project_file'] = {}
        return proj_json
class SToVLoop:
    def __init__(self,lstart, lend, count, remain, midi_PC=None):
        self.loop = [lstart, lend, count, remain, midi_PC]
    def rtn_json(self):
        loop_dict = {}
        loop_dict['type'] = "loop"
        loop_dict['lstart'] = self.loop[0]
        loop_dict['lend'] = self.loop[1]
        loop_dict['count'] = self.loop[2]
        loop_dict['remain'] = self.loop[3]
        loop_dict['midi_PC'] = self.loop[4]
        return ["loop",loop_dict]


