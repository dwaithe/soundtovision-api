ASSET_TYPES = ['text', 'video', 'photo', 'reactive', 'stack']
INT_METHODS = ['linear','none','step', 'steps','easeInSine','easeOutSine','easeInOutSine','easeInQuad','easeOutQuad','easeInOutQuad','easeInCubic','easeOutCubic','easeInOutCubic','easeInQuart','easeOutQuart','easeInOutQuart','easeInQuint','easeOutQuint','easeInOutQuint','easeInExpo','easeOutExpo','easeInOutExpo','easeInCirc','easeOutCirc','easeInOutCirc','easeInBack','easeOutBack','easeInOutBack','easeInElastic','easeOutElastic','easeInOutElastic','easeInBounce','easeOutBounce','easeInOutBounce']
import math
class SToVAsset:
    def __init__(self, asset_ref, atype, astart, aend, x, y, width, height, type_params):
        
        self.atype = atype
         
        self.asset_ref = asset_ref
        self.label = ['local',atype]

        self.dtype = {'mp4':'video','mov':'video','png':'photo','zip':'stack'}
        self.idtype = {'reactive':1,'video':12,'photo':18, 'stack': 20}


        self.pw = 960
        self.ph = 540

        if('prim_type' in type_params):
            self.id_num = 34
            self.pw = width
            self.ph = height
        else:
            self.id_num = self.idtype[atype]


        self.props_array = ['x', 'y', 'width', 'height', 'rotation', 'alpha']
        self.props = {}
        self.type_params = type_params

        if(self.atype == 'stack'):
            self.props_array.append('trans')
        
        for prop in self.props_array:
            self.props[prop+'_enabled'] = [False]
            self.props[prop+'_method'] = [0]
            self.props[prop+'_cutoff'] = [0]
            self.props[prop+'_gain'] = [1]
            self.props[prop+'_signal'] = [0]
            self.props[prop+'_inter'] = ['linear']
            self.props[prop+'_trigenabled'] = [False]
            self.props[prop+'_trigsignal'] = [0]
            self.props[prop+'_triggain'] = [0]
            self.props[prop+'_trigthr'] = [0]
            self.props[prop+'_trigmode'] = [False]
            self.props[prop+'_trigchannel'] = [0]
            self.props[prop+'_envselect'] = [0]
            self.props[prop+'_envduration'] = [0]

        if(self.atype == 'stack'):
            self.props['simg'] = [0]
            self.props['trans_type'] = ['None']
            


        if self.id_num == 34:
            self.tint = ['#FFFFFF']
        else:
            self.tint = False

        
        
        
        self.astart = astart
        self.aend = aend
        self.ypos = 0
        self.zIndex = 0
        self.layer = 0
        
        self.asset_duration = aend-astart
        self.toStream = True
            
        self.x = [x]
        self.y = [y]
        self.height = [height]
        self.width = [width]
        self.rotation = [0]
        self.alpha = [1]
        self.flip_vert = False
        self.flip_horz = False
        
        self.keyframes = ['0.000']
        self.key = 0

        self.start_offset = 0
        self.filter = 'None'
        self.filters = []
        
    def add_keyframe(self, time):
        
        self.keyframes.append(str(time))
        
        leng = self.x.__len__()-1
        self.x.append(self.x[leng])
        self.y.append(self.y[leng])
        self.height.append(self.height[leng])
        self.width.append(self.width[leng])
        self.rotation.append(self.rotation[leng])
        self.alpha.append(self.alpha[leng])

        
        for prop in self.props_array:
            self.props[prop+'_enabled'].append(False)
            self.props[prop+'_method'].append(0)
            self.props[prop+'_cutoff'].append(0)
            self.props[prop+'_gain'].append(1)
            self.props[prop+'_signal'].append(0)
            self.props[prop+'_inter'].append('linear')
            self.props[prop+'_trigenabled'].append(False)
            self.props[prop+'_trigsignal'].append(0)
            self.props[prop+'_triggain'].append(0)
            self.props[prop+'_trigthr'].append(0)
            self.props[prop+'_trigmode'].append(False)
            self.props[prop+'_trigchannel'].append(0)
            self.props[prop+'_envselect'].append(0)
            self.props[prop+'_envduration'].append(0)

        if(self.atype == 'stack'):
            self.props['simg'].append(len(self.props['simg']))
            self.props['trans_type'].append('None')

        if self.id_num == 34:
            self.tint.append('#FFFFFF')

    def set_position(self,key, x, y , width, height):
        self.x[key] = x
        self.y[key] = y
        self.width[key] = width
        self.height[key] = height
        
    @property
    def layer(self):
        return self._layer
    @layer.setter
    def layer(self, value):
        self.ypos = int(value)
        self.zIndex =  int(value)
        self._layer = int(value)

    
    def add_filter(self, value):
        assert isinstance(value, str)
        self.filters.append(value)
        self.filter = value
    @property
    def flip_vert(self):
        return self._flip_vert
    @flip_vert.setter
    def flip_vert(self, value):
        self._flip_vert = bool(value)
    @property
    def flip_horz(self):
        return self._flip_horz
    @flip_horz.setter
    def flip_horz(self, value):
        self._flip_horz = bool(value)
    @property
    def astart(self):
        return self._astart
    @astart.setter
    def astart(self, value):
        self._astart = float(value)
    @property
    def aend(self):
        return self._aend
    @aend.setter
    def aend(self, value):
        self._aend = float(value)          
    @property
    def atype(self):
        return self._atype
    @atype.setter
    def atype(self, value):
        assert isinstance(value, str)
        assert value in ASSET_TYPES
        self._atype = value
        
    def get_x(self, key):
        return self.x[key]
    def set_x(self, key, value):
        self.x[key] = float(value)
        
    def get_y(self, key):
        return self.y[key]
    def set_y(self, key, value):
        self.y[key] = float(value)
    
    def get_height(self, key):
        return self.height[key]
    def set_height(self, key, value):
        self.height[key] = float(value)
        
    def get_width(self, key):
        return self.width[key]
    def set_width(self, key, value):
        self.width[key] = float(value)
    
    def get_height(self, key):
        return self.height[key]
    def set_height(self, key, value):
        self.height[key] = float(value)
        
    def get_rotation(self, key):
        return self.rotation[key]
    def set_rotation(self, key, value):
        self.rotation[key] = math.pi*float(value)/180.
    
    def get_alpha(self, key):
        return self.alpha[key]
    def set_alpha(self, key, value):
        self.alpha[key] = float(value)
    
    def get_prop_enabled(self, prop, key):
        return self.props[prop+'_enabled'][key]
    def set_prop_enabled(self, prop, key, value):
        self.props[prop+'_enabled'][key] = bool(value)
        
    def get_prop_method(self, prop, key):
        return self.props[prop+'_method'][key]
    def set_prop_method(self, prop, key, value):
        self.props[prop+'_method'][key] = int(value)
        
    def get_prop_cutoff(self, prop, key):
        return self.props[prop+'_cutoff'][key]
    def set_prop_cutoff(self, prop, key, value):
        self.props[prop+'_cutoff'][key] = float(value)
        
    def get_prop_gain(self, prop, key):
        return self.props[prop+'_gain'][key]
    def set_prop_gain(self, prop, key, value):
        self.props[prop+'_gain'][key] = float(value)
        
    def get_prop_signal(self, prop, key):
        return self.props[prop+'_signal'][key]
    def set_prop_signal(self, prop, key, value):
        self.props[prop+'_signal'][key] = int(value)
        
    def get_prop_interpolate(self, prop, key):
        return self.props[prop+'_inter'][key]
    def set_prop_interpolate(self, prop, key, value):
        assert isinstance(value, str)
        assert value in INT_METHODS
        self.props[prop+'_inter'][key] = value
        
    def get_prop_trigger_enabled(self, prop, key):
        return self.props[prop+'_trigenabled'][key]
    def set_prop_trigger_enabled(self, prop, key, value):
        self.props[prop+'_trigenabled'][key] = bool(value)
    
    def get_prop_trigger_signal(self, prop, key):
        return self.props[prop+'_trigsignal'][key]
    def set_prop_trigger_signal(self, prop, key, value):
        self.props[prop+'_trigsignal'][key] = int(value)
        
    def get_prop_trigger_gain(self, prop, key):
        return self.props[prop+'_triggain'][key]
    def set_prop_trigger_gain(self, prop, key, value):
        self.props[prop+'_triggain'][key] = float(value)
        
    def get_prop_trigger_threshold(self, prop, key):
        return self.props[prop+'_trigthr'][key]
    def set_prop_trigger_threshold(self, prop, key, value):
        self.props[prop+'_trigthr'][key] = float(value)
    
    def get_prop_trigger_mode(self, prop, key):
        return self.props[prop+'_trigmode'][key]
    def set_prop_trigger_mode(self, prop, key, value):
        self.props[prop+'_trigmode'][key] = bool(value)


    def get_prop_trigger_channel(self, prop, key):
        return self.props[prop+'_trigchannel'][key]
    def set_prop_trigger_channel(self, prop, key, value):
        self.props[prop+'_trigchannel'][key] = int(value)

    def get_prop_envelope_select(self, prop, key):
        return self.props[prop+'_envselect'][key]
    def set_prop_envelope_select(self, prop, key, value):
        self.props[prop+'_envselect'][key] = int(value)

    def get_prop_envelope_duration(self, prop, key):
        return self.props[prop+'_envduration'][key]
    def set_prop_envelope_duration(self, prop, key, value):
        self.props[prop+'_envduration'][key] = float(value)
    def get_prop_simg(self,key):
        return self.props['simg'][key]
    def set_prop_simg(self,key,value):
        self.props['simg'][key] = int(value)
    def get_prop_trans_type(self,key):
        return self.props['trans_type'][key]
    def set_prop_trans_type(self,key,value):
        self.props['trans_type'][key] = int(value)
    
    def rtn_json(self):
        
        asset_dict = {}
        asset_dict["idNum"] = self.id_num
        asset_dict['type'] = self.atype
        asset_dict['label'] = self.label
        asset_dict['filter'] = self.filter
        asset_dict['filters'] = self.filters


        asset_dict['x'] = []
        asset_dict['y'] = []
        asset_dict['width'] = []
        asset_dict['height'] = []
        for i in range(0,len(self.keyframes)):
            asset_dict['x'].append(self.x[i]/2)
            asset_dict['y'].append(self.y[i]/2)
            asset_dict['width'].append(self.width[i]/2)
            asset_dict['height'].append(self.height[i]/2)
        
        asset_dict['pw'] = self.pw
        asset_dict['ph'] = self.ph
        
        asset_dict['rotation'] = self.rotation
        asset_dict['alpha'] = self.alpha

        if self.tint:
            asset_dict['tint'] = self.tint
        
        asset_dict['params'] = self.type_params
        asset_dict['start_offset'] = self.start_offset
        
        asset_dict['keyframes'] = self.keyframes
        asset_dict['key'] = self.key
        asset_dict['zIndex'] = self.zIndex
        asset_dict['ypos'] = self.ypos
        
        asset_dict['flip_vert'] = self.flip_vert
        asset_dict['flip_horz'] = self.flip_horz
        

        
        for prop in self.props_array:
            asset_dict[prop+'_enabled'] = self.props[prop+'_enabled']
            asset_dict[prop+'_method'] = self.props[prop+'_method']
            asset_dict[prop+'_cutoff'] = self.props[prop+'_cutoff']
            asset_dict[prop+'_gain'] = self.props[prop+'_gain']
            asset_dict[prop+'_signal'] = self.props[prop+'_signal']
            asset_dict[prop+'_inter'] = self.props[prop+'_inter']
            asset_dict[prop+'_trigenabled'] = self.props[prop+'_trigenabled']
            asset_dict[prop+'_trigsignal'] = self.props[prop+'_trigsignal']
            asset_dict[prop+'_triggain'] = self.props[prop+'_triggain']
            asset_dict[prop+'_trigthr'] = self.props[prop+'_trigthr']
            asset_dict[prop+'_trigmode'] = self.props[prop+'_trigmode']
            asset_dict[prop+'_trigchannel']  = self.props[prop+'_trigchannel']
            asset_dict[prop+'_envselect'] = self.props[prop+'_envselect']
            asset_dict[prop+'_envduration'] = self.props[prop+'_envduration']


        if(self.atype == 'stack'):
            asset_dict['simg'] = self.props['simg']
            asset_dict['trans_type'] = self.props['trans_type']

            
        asset_dict['astart'] = self.astart
        asset_dict['aend'] = self.aend
        asset_dict['asset_duration'] = self.asset_duration
        asset_dict['toStream'] = self.toStream

        return [self.asset_ref, asset_dict]