import wave
import torch
import struct
import numpy as np
import subprocess
import time

class WaveLoader:
    def __init__(self, wave_file_name):
        self.wave_file_name = wave_file_name
        self.wr = wave.open(self.wave_file_name, 'rb')
        print(self.wr.getparams())

    def __del__(self):
        try:
            self.wr.close()
        except Exception as e:
            print('Error %s', str(e))

    def get_sample(self):
        if self.wr.tell() == self.wr.getnframes():
            self.wr.rewind()
        sample_rate = self.wr.getframerate()
        frame = self.wr.readframes(sample_rate)
        if len(frame) < sample_rate:  # if we get a part sample just loop back over again
            self.wr.rewind()
            frame = self.wr.readframes(sample_rate)
        fmt = '<%dh' % sample_rate
        frame_iter = struct.unpack(fmt, frame)
        _data = list(frame_iter)
        data = torch.tensor(_data)
        if self.wr.tell() == self.wr.getnframes():
            self.wr.rewind()
        frame = self.wr.readframes(sample_rate)
        if len(frame) < sample_rate:
            self.wr.rewind()
            frame = self.wr.readframes(sample_rate)
        frame_iter = struct.unpack(fmt, frame)
        _data = list(frame_iter)
        label = torch.tensor(_data)
        return data, label

    def write_wave(self, tensors, file_name, nchannels, sampwidth, framerate):
        _list = tensors.tolist()
        ww = wave.open(file_name, 'wb')
        ww.setnchannels(nchannels)
        ww.setsampwidth(sampwidth)
        ww.setframerate(framerate)
        fmt = '<%dh' % framerate
        for sample in _list:
            slist = np.short(sample).tolist()
            blist = struct.pack(fmt, *slist)
            ww.writeframesraw(blist)

    def play_sample_bytes(self, sample_bytes):
        proc = subprocess.Popen("sox -traw -r 8000 -b 16 -e signed -c 1 - -tcoreaudio", stdin=subprocess.PIPE,
                         shell=True)
        time.sleep(3)
        proc.communicate(sample_bytes)


    def play_sample_tensor(self, tensors, nchannels, sampwidth, framerate):
        _list = tensors.tolist()
        fmt = '<%dh' % framerate
        bytes_out = bytearray()
        for sample in _list:
            slist = np.short(sample).tolist()
            bytes_out += struct.pack(fmt, *slist)
        self.play_sample_bytes(bytes_out)
