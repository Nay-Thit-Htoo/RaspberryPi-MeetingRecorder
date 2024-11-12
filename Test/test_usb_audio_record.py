import pyaudio
import wave

# Define parameters for recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1               # Number of audio channels (1 for mono)
RATE = 44100               # Sampling rate (in Hz)
CHUNK = 1024               # Buffer size
WAVE_OUTPUT_FILENAME = "output.wav"  # Output file name

# Create a PyAudio object
p = pyaudio.PyAudio()

# Open the stream for recording
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=1)  # Replace with your USB microphone's device index

print("Recording...")

frames = []

try:
    # Record for 5 seconds (you can change this duration)
    for i in range(0, int(RATE / CHUNK * 5)):
        data = stream.read(CHUNK)
        frames.append(data)
except KeyboardInterrupt:
    # Stop recording on keyboard interrupt
    print("Recording stopped.")

# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()

# Save the recorded data as a WAV file
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Recording saved as {WAVE_OUTPUT_FILENAME}.")
