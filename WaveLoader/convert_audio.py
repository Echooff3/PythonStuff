#!/Users/john.skibicki/anaconda3/bin/python
from os.path import join
from os.path import basename
from glob import glob
import subprocess


# sox input.wav -r 8000 -c 1 output.wav

for ext in ('*.wav', '*.mp3', '*.ogg'):
    for x in glob(join("./audio", ext)):
        print(basename(x))
        subprocess.run(["sox", x, '-r', '8000', '-c', '1', join('./audio-converted', basename(x))])


# sox_audio = subprocess.Popen( "sox -traw -r 44100 -b 8 -e signed - -tcoreaudio", stdin=subprocess.PIPE, shell=True )