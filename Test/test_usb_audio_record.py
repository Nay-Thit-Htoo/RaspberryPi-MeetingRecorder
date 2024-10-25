import pyaudio
import numpy as np
from scipy.io.wavfile import write
import threading

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048  # Increased chunk size
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

def record_audio(frames):
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        except IOError as e:
            print(f"Input overflowed: {e}")

# Start recording in a separate thread
record_thread = threading.Thread(target=record_audio, args=(frames,))
record_thread.start()

# Record for a set duration
threading.Timer(RECORD_SECONDS, lambda: stream.stop_stream()).start()
record_thread.join()  # Wait for the recording thread to finish

print("Finished recording.")

# Stop and close the stream
stream.close()
audio.terminate()

# Save the recorded data as a WAV file
wave_data = b''.join(frames)
write(WAVE_OUTPUT_FILENAME, RATE, np.frombuffer(wave_data, dtype=np.int16))

print(f"Audio saved to {WAVE_OUTPUT_FILENAME}")
