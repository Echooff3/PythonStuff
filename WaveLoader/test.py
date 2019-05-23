from WaveLoader import WaveLoader
import torch

# sox convert
# sox input.wav -r 8000 output.wav

sample = './pemex8k.wav'
wl = WaveLoader(sample)  # type WaveLoader
data, label = wl.get_sample()

print(data.shape, label.shape)

# Write junk
t = torch.rand((5, 8000))
t = torch.mul(t, 65535)
t = torch.sub(t, 65535/2)

wl.write_wave(t, './output.wav', 1, 2, 8000)


#write pemex
buff = [data.tolist()]
for x in range(5):
    data, label = wl.get_sample()
    buff.append(data.tolist())

pemex = torch.tensor(buff)
wl.write_wave(pemex, './output-pemex.wav', 1, 2, 8000)