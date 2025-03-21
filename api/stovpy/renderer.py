import math
import json
import os
import socketio
import shutil
import numpy as np
import psutil



 
class SToVRender:
    def __init__(self, project_file, document_settings, render_settings, offline_wave=None):
        
        self.fps = render_settings['fps']
        self.start_time = render_settings['start_time']
        self.end_time = render_settings['end_time']
        self.render_id = render_settings['render_id']
        
        self.limit_rate = render_settings['limit_rate']
        self.num_cores = render_settings['num_cores']
        if('sample_rate' in render_settings):
            self.sample_rate = render_settings['sample_rate']
        else: 
            render_settings['sample_rate'] = 48000
        self.sample_rate = render_settings['sample_rate']
        
        if('fftSize' in render_settings):
            self.fft_size = render_settings['fftSize']
        else: 
            render_settings['fftSize'] = 512
        self.fft_size = render_settings['fftSize']
        
        if offline_wave != None:
            self.offline_wave = offline_wave
            self.audio = True
        else:
            self.audio = False
        self.render_settings = render_settings
        
        self.sec_dur = 5000
        self.total_frames = round(self.fps*(self.end_time-self.start_time),0)
        self.end_sec = math.floor(self.total_frames/self.fps)
        
        
        self.rparams = {}
        self.rparams['data'] = project_file
        self.rparams['document_settings'] = document_settings
        self.rparams['render_settings'] = self.render_settings
        self.rparams['total_frames_arr'] = []
        self.rparams['start_arr'] = []
        self.rparams['end_arr'] = []
        self.rparams['num_arr'] = []
        
        self.gen_reg = []
        self.gen_reg.append("[0,null,null,1,4./60,0,'Sin Example',0,duration]")
        self.gen_reg.append("[1,null,null,1,1./60,0,'Square Example',0,duration]")
        self.gen_reg.append("[2,null,null,1,8./60,0,'Triangle Example',0,duration]")
        self.gen_reg.append("[3,null,null,1,8./60,0,'Sawtooth Example',0,duration]")
        
        self.sig_reg = []
        self.sig_reg.append("['integrate',null,null,Math.round(this.fftSize/2),Math.round(0),'volume',0,duration]")
        self.sig_reg.append("['max',null,null,Math.round(this.fftSize/2),Math.round(0),'max',0,duration]")
        self.sig_reg.append("['integrate',null,null,Math.round((this.fftSize/2)/3),Math.round(0),'int lower Hz',0,duration]")
        self.sig_reg.append("['integrate',null,null,Math.round(2*(this.fftSize/2)/3),Math.round((this.fftSize/2)/3),'int middle Hz',0,duration]")
        self.sig_reg.append("['integrate',null,null,Math.round(this.fftSize/2),Math.round(2*(this.fftSize/2)/3),'int higher Hz',0,duration]")
        self.sig_reg.append("['max',null,null,Math.round((this.fftSize/2)/3),Math.round(0),'max lower Hz',0,duration]")
        self.sig_reg.append("['max',null,null,Math.round(2*(this.fftSize/2)/3),Math.round((this.fftSize/2)/3),'max middle Hz',0,duration]")
        self.sig_reg.append("['max',null,null,Math.round(this.fftSize/2),Math.round(2*(this.fftSize/2)/3),'max higher Hz',0,duration]")
        self.sig_reg.append("['thr_integrate',null,null,Math.round(this.fftSize/2),Math.round(0),'Trigger int',0,duration]")

        
        self.num_of_segs = math.ceil(self.total_frames/((self.sec_dur/1000)*self.fps))
        
        total_frames_seg = self.fps*(self.sec_dur/1000)
        for it in range(0, self.num_of_segs):

            if total_frames_seg * (it+1) > self.total_frames:
                total_frames_seg = self.total_frames-(total_frames_seg*it)
            else:
                total_frames_seg = self.fps*(self.sec_dur/1000)


            self.rparams['total_frames_arr'].append(total_frames_seg)
            start_time = self.start_time+it*(self.sec_dur/1000)
            self.rparams['start_arr'].append(start_time)
            self.rparams['end_arr'].append(start_time + (self.sec_dur/1000))
            self.rparams['num_arr'].append(it)


        self.rparams['num_of_segs'] = self.num_of_segs
        self.rparams['render_id'] = self.render_id
        self.rparams['fps'] = self.fps
        self.rparams['audio'] = self.audio
        
        self.rparams['gen_sig_reg'] = json.dumps(self.gen_reg)
        self.rparams['sig_sig_reg'] = json.dumps(self.sig_reg)


        ## MIDI:
        self.rparams['mid_rec'] = json.dumps([])
        self.rparams['ov_offset'] = json.dumps([])
        
      
            

            
        
    def start_render(self):
        
        #This sends the signal to render a section.
        self.sio = socketio.SimpleClient()
        self.sio.connect('http://localhost:3033')
        self.sio.emit('init_render',{'num_of_segs':self.num_of_segs,'num_cores':self.num_cores,'limit_rate':self.limit_rate})

        renderer_details = self.sio.receive()
        while renderer_details[0] != "renderer_details":
            renderer_details = self.sio.receive()
        assert renderer_details[0] == 'renderer_details',"Something unexpected happened whilst communicating with renderer."
         
        self.temp_path = renderer_details[1]['temp_dir']
        
        if self.audio == True:
            dest_path = os.path.join(self.temp_path,'..',self.render_id+'_song.ogg')
            self.offline_wave.save_ogg(dest_path,self.start_time,self.end_time)
            st_curr = self.start_time*self.sample_rate/self.fft_size
            st_end = (self.end_sec)*self.sample_rate/self.fft_size
            interval = (self.sec_dur/1000)*self.sample_rate/self.fft_size
            byte_frequency_data, sample_rate = self.offline_wave.process_wave_file(self.fft_size, 0.0)
            self.rparams['frequencyBinCount'] = byte_frequency_data[0].__len__()
            print('self.num_of_segs',self.num_of_segs)
            for i in range(0,self.num_of_segs-1):
                flattened_array = []
                for c in range(math.floor(st_curr+(interval*i)),math.ceil(st_curr+(interval*(i+1)))):
                    flattened_array.extend(np.round(byte_frequency_data[c]).astype(np.uint8))
                file_name = f"{self.rparams['render_id']}_{i}_song.bin"
                binary_data = bytes(flattened_array)
                with open(os.path.join(self.temp_path,'..',file_name), "wb") as f:
                    f.write(binary_data)

            flattened_array = []
            for c in range(math.floor(st_curr+(interval*(self.num_of_segs-1))),math.ceil(st_curr+st_end)+60):
                flattened_array.extend(np.round(byte_frequency_data[c]).astype(np.uint8))
            file_name = f"{self.rparams['render_id']}_{self.num_of_segs-1}_song.bin"
            binary_data = bytes(flattened_array)
            with open(os.path.join(self.temp_path,'..',file_name), "wb") as f:
                f.write(binary_data)
        
        self.sio.emit('render_segments', self.rparams)
        render_progress = self.sio.receive()
        mem_arr = []
        fps_arr = []
        while render_progress[0] != "send_back_complete":
            percent = render_progress[1]['progress']
            render_fps = render_progress[1]['render_fps']
            bars = "#"*int(percent/4)+" "*int((100-percent)/4)
            process_name = "node"  # Change this to the process name you want to monitor
            mem_sum = 0
            for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
                try:
                    if proc.info['name'] and process_name in proc.info['name'].lower():
                        mem_sum += proc.info['memory_info'].rss / 1024**2

                except:
                    pass

            mem_arr.append(mem_sum)
            fps_arr.append(render_fps)
            print("\r render progress: ["+bars+"] "+str(round(percent,2))+"% FPS: "+str(render_fps), end="")
            render_progress = self.sio.receive()

        src = self.temp_path+"/s2v-"+self.render_id+".mp4"
        dst = "test_outputs/s2v-"+self.render_id+".mp4"
        shutil.copyfile(src, dst)
        print(' complete')
        return mem_arr, fps_arr