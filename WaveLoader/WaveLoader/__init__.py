import wave
import torch
import struct


class WaveLoader:
    def __init__(self, wave_file_name):
        self.wave_file_name = wave_file_name
        self.wr = wave.open(self.wave_file_name, 'rb')

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
        frame_iter = struct.iter_unpack('<h', frame)
        _data = [x[0] for x in frame_iter]
        data = torch.tensor(_data)
        if self.wr.tell() == self.wr.getnframes():
            self.wr.rewind()
        frame = self.wr.readframes(sample_rate)
        frame_iter = struct.iter_unpack('<h', frame)
        _data = [x[0] for x in frame_iter]
        label = torch.tensor(_data)
        return data, label
