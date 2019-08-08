from pydub import AudioSegment
sound = AudioSegment.from_file("D:/lyrico/media/audio/young")
sound.export("D:/lyrico/media/audio/youngpy.mp3", format="mp3", bitrate="128k")