import numpy as np
from scipy.fft import rfft, rfftfreq
from pydub import AudioSegment

import matplotlib.pyplot as plt

class SToVAudio:
    def __init__(self, filename):

        self.audio_seg = AudioSegment.from_wav(filename)

        num_channels = self.audio_seg.channels
        self.sample_rate = self.audio_seg.frame_rate
        self.sample_width = self.audio_seg.sample_width
        num_frames = self.audio_seg.frame_count()
        

        wave_data = np.array(self.audio_seg.get_array_of_samples(), dtype=np.float32).reshape((-1, self.audio_seg.channels)) / (
                1 << (8 * self.sample_width - 1))

        print(wave_data.shape)
        if num_channels > 1:
            #wave_data = wave_data.reshape(-1, num_channels)
            wave_data = np.mean(wave_data, axis=1)

        self.mono_data = wave_data

    def linear_to_decibels(self, linear_value):
        return 20 * np.log10(linear_value)

    def get_byte_frequency_data(self, magnitude_buffer, min_decibels=-90.0, max_decibels=-10.0):
        # Convert from linear magnitude to decibels
        db_magnitudes = np.where(magnitude_buffer > 0, self.linear_to_decibels(magnitude_buffer), min_decibels)

        # Clip the decibel values to the range [min_decibels, max_decibels]
        db_magnitudes = np.clip(db_magnitudes, min_decibels, max_decibels)

        # Scale decibels to byte range [0, 255]
        range_scale_factor = 1 / (max_decibels - min_decibels)
        scaled_values = 255 * (db_magnitudes - min_decibels) * range_scale_factor

        # Clip to byte range [0, 255] and convert to unsigned 8-bit integers
        byte_values = list(np.clip(scaled_values, 0, 255))

        return byte_values

    def process_wave_file(self, fft_size, smoothing_time_constant=0.0):
        # Read the wave file
        audio_data = self.mono_data
        # Initialize the magnitude buffer for smoothing
        magnitude_buffer = np.zeros(512//2+1)
        # Calculate the FFT on the audio data
        byte_freq_data = []
        for i in range(0,audio_data.shape[0]-fft_size,fft_size):
            windowed_data = audio_data[i:i+fft_size] * np.blackman(fft_size)
            fft_result = rfft(windowed_data)
            # Calculate the magnitudes and normalize
            magnitudes = np.abs(fft_result) / fft_size

            # Smoothing with previous result
            k = smoothing_time_constant
            magnitude_buffer = k * magnitude_buffer + (1 - k) * magnitudes

            # Get byte frequency data
            byte_freq_data.append(self.get_byte_frequency_data(magnitude_buffer))
        
        return byte_freq_data, self.sample_rate
    def save_ogg(self, dst_path, start_time, end_time):

           seg = self.audio_seg[start_time*1000:end_time*1000]
           seg.export(dst_path, format="ogg")

