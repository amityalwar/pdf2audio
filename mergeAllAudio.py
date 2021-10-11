from pydub import AudioSegment
from pathlib import Path
import ffmpeg

AudioSegment.converter = r'C:\Users\amity\Desktop\Personal\PDF2Audio\PDF2Audio\ffmpeg-2021-10-07-git-b6aeee2d8b-essentials_build\bin\ffmpeg.exe'
DIRECTORY  = Path(r'C:\Users\amity\Desktop\Personal\PDF2Audio\PDF2Audio\HC')
playlist = [AudioSegment.from_mp3(mp3_file) for mp3_file in DIRECTORY.glob("*.mp3")] 

combined = AudioSegment.empty()

for song in playlist:
    combined += song

combined.export(r"C:\Users\amity\Desktop\Personal\PDF2Audio\PDF2Audio\HC\HiddenCosts.mp3", format="mp3")
print('Great Success!!')