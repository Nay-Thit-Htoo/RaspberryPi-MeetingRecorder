import pyaudio
import subprocess
import wave
import threading
import queue

# Constants
CHANNELS = 1
RATE = 44100
CHUNK = 1024
FORMAT = pyaudio.paInt16

# Initialize a queue to handle audio chunks
audio_queue = queue.Queue()

# Function to capture audio from the microphone
def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        audio_queue.put(data)

# Function to process audio with SoX and play it back
def process_and_play_audio():
    p = pyaudio.PyAudio()
    stream_out = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

    while True:
        if not audio_queue.empty():
            # Get a chunk from the queue
            audio_chunk = audio_queue.get()

            # Process the chunk with SoX
            # Using `subprocess` to call SoX for effects
            process = subprocess.Popen(
                ["sox", "-t", "raw", "-b", "16", "-e", "signed-integer", "-r", str(RATE), "-c", str(CHANNELS), "-",
                 "-t", "raw", "-", "gain", "-3"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)

            processed_audio, _ = process.communicate(audio_chunk)

            # Play the processed audio chunk
            stream_out.write(processed_audio)

# Start threads for recording and playback
record_thread = threading.Thread(target=record_audio)
play_thread = threading.Thread(target=process_and_play_audio)

record_thread.start()
play_thread.start()

# Join threads (optional, for example purposes)
record_thread.join()
play_thread.join()
