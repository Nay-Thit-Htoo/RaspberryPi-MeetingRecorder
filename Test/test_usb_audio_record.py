import pyaudio
import numpy as np
from scipy.io.wavfile import write

# Parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1               # Number of audio channels
RATE = 44100               # Sample rate (samples per second)
CHUNK = 1024               # Number of frames per buffer
RECORD_SECONDS = 5         # Duration of recording
WAVE_OUTPUT_FILENAME = "output.wav"  # Output file name

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded data as a WAV file
wave_data = b''.join(frames)
write(WAVE_OUTPUT_FILENAME, RATE, np.frombuffer(wave_data, dtype=np.int16))

print(f"Audio saved to {WAVE_OUTPUT_FILENAME}")
