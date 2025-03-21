import copy
import json
import os

class SToVFilter:
    def __init__(self, filter_ref, active):
        
        self.id_num = 0
        self.ftype = "filter"
        self.filter_ref = filter_ref
        self.label = ["filter"]

        module_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(module_dir, "filters_df.json")
        with open(json_path, "r") as f:
            filter_defaults = json.load(f)


        self.name = copy.deepcopy(filter_defaults[filter_ref]['name'])
        self.fn =  copy.deepcopy(filter_defaults[filter_ref]['fn'])
        self.active = active
        self.params = copy.deepcopy(filter_defaults[filter_ref]['params'])
        
        for prop in self.params:

            self.params[prop]['signal'] = [0]
            self.params[prop]['cutoff'] = [0]
            self.params[prop]['gain'] = [1]
            self.params[prop]['enabled'] = [False]
            self.params[prop]['method'] = [0]
            self.params[prop]['inter'] = ["linear"]
            self.params[prop]['trigenabled'] = [False]
            self.params[prop]['trigsignal'] = [0]
            self.params[prop]['triggain'] = [0]
            self.params[prop]['trigthr'] = [0]
            self.params[prop]['trigmode'] = [False]
    
    def get_prop_value(self, prop):
        return self.params[prop]['default']
    def set_prop_value(self, prop, value):
        self.params[prop]['default'] = value

    def get_prop_enabled(self, prop):
        return self.params[prop]['enabled']
    def set_prop_enabled(self, prop, value):
        self.params[prop]['enabled'] = [value]
    def get_prop_method(self, prop):
        return self.params[prop]['method']
    def set_prop_method(self, prop, value):
        self.params[prop]['method'] = [value]
    def get_prop_gain(self, prop):
        return self.params[prop]['gain']
    def set_prop_gain(self, prop, value):
        self.params[prop]['gain'] = [value]
    def get_prope_cutoff(self, prop):
        return self.params[prop]['cutoff']
    def set_prop_cutoff(self, prop, value):
        self.params[prop]['cutoff'] = [value]
    def get_prop_signal(self, prop):
        return self.params[prop]['signal']
    def set_prop_signal(self, prop, value):
        self.params[prop]['signal'] = [value]

    def get_prop_interpolate(self, prop):
        return self.params[prop]['inter']
    def set_prop_interpolate(self, prop, value):
        self.params[prop]['inter'] = [value]

    def get_prop_trigger_enabled(self, prop):
        return self.params[prop]['trigenabled']
    def set_prop_trigger_enabled(self, prop, value):
        self.params[prop]['trigenabled'] = [value]
    def get_prop_trigger_signal(self, prop):
        return self.params[prop]['trigsignal']
    def set_prop_trigger_signal(self, prop, value):
        self.params[prop]['trigsignal'] = [value]
    def get_prop_trigger_gain(self, prop):
        return self.params[prop]['triggain']
    def set_prop_trigger_gain(self, prop, value):
        self.params[prop]['triggain'] = [value]
    def get_prop_trigger_threshold(self, prop):
        return self.params[prop]['trigthr']
    def set_prop_trigger_threshold(self, prop, value):
        self.params[prop]['trigthr'] = [value]
    def get_prop_trigger_mode(self, prop):
        return self.params[prop]['trigmode']
    def set_prop_trigger_mode(self, prop, value):
        self.params[prop]['trigmode'] = [value]
    
    def rtn_json(self):
        
        filter_dict = {}
        filter_dict["idNum"] = self.id_num
        filter_dict['type'] = self.ftype
        filter_dict['label'] = self.label
        filter_dict['name'] = self.name
        filter_dict['fn'] = self.fn
        filter_dict['active'] = self.active
        filter_dict['params'] = self.params
         
        return [self.filter_ref, filter_dict]