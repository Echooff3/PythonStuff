from WaveLoader import WaveLoader

sample = './pemex000.wav'
wl = WaveLoader(sample)  # type WaveLoader
data, label = wl.get_sample()

print(data.shape, label.shape)
