import pyaudio
import wave
import subprocess
import threading
import queue
import os
from datetime import datetime

# Audio configurations
CHANNELS = 1
RATE = 44100
CHUNK = 1024
FORMAT = pyaudio.paInt16
OUTPUT_FILE = f"processed_audio_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.wav"

# Queue to hold audio chunks
audio_queue = queue.Queue()

# Function to capture audio from the microphone
def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("[Audio] Recording started...")
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_queue.put(data)

# Function to process and save audio with SoX
def process_and_save_audio():
    p = pyaudio.PyAudio()
    
    # Open a wave file for output
    with wave.open(OUTPUT_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        
        print("[Audio] Saving processed audio...")
        while True:
            if not audio_queue.empty():
                audio_chunk = audio_queue.get()

                # Process the audio chunk using SoX (with a gain effect as an example)
                process = subprocess.Popen(
                    ["sox", "-t", "raw", "-b", "16", "-e", "signed-integer", "-r", str(RATE), "-c", str(CHANNELS), "-",
                     "-t", "raw", "-", "gain", "-3"],  # Apply a gain effect of -3 dB
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE
                )

                # Send audio chunk to SoX for processing
                processed_audio, _ = process.communicate(audio_chunk)

                # Write the processed audio to the output file
                wf.writeframes(processed_audio)

        print(f"[Audio] Audio saved to {OUTPUT_FILE}")

# Start the recording and processing in separate threads
record_thread = threading.Thread(target=record_audio)
save_thread = threading.Thread(target=process_and_save_audio)

record_thread.start()
save_thread.start()

# Wait for threads to finish
record_thread.join()
save_thread.join()
