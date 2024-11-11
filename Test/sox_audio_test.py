import tkinter as tk
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
OUTPUT_FILE = "processed_audio.wav"

# Initialize a queue to handle audio chunks
audio_queue = queue.Queue()

# AudioRecorder class for handling recording, SoX processing, and saving
class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = queue.Queue()  # Use a queue to buffer audio data
        self.recording = False
        self.record_thread = None
        self.process_thread = None
        self.is_processing = False

    def start_recording(self):
        if self.recording:
            print("Recording is already in progress.")
            return

        self.recording = True

        def record():
            try:
                self.stream = self.audio.open(format=FORMAT,
                                              channels=CHANNELS,
                                              rate=RATE,
                                              input=True,
                                              input_device_index=1,
                                              frames_per_buffer=CHUNK)

                print("[Audio] Recording started...")
                while self.recording:
                    data = self.stream.read(CHUNK, exception_on_overflow=False)
                    audio_queue.put(data)  # Add data to the queue
            except Exception as e:
                print(f"Error recording audio: {e}")
            finally:
                if self.stream is not None:
                    self.stream.stop_stream()
                    self.stream.close()
                    self.save_wave()

        self.record_thread = threading.Thread(target=record)
        self.record_thread.start()

        # Start audio processing in another thread
        self.is_processing = True
        self.process_thread = threading.Thread(target=self.process_audio)
        self.process_thread.start()

    def stop_recording(self):
        self.recording = False
        if self.record_thread is not None:
            self.record_thread.join()

        # Stop the processing thread if recording has stopped
        self.is_processing = False
        if self.process_thread is not None:
            self.process_thread.join()

        print("[Audio] Recording stopped.")

    def process_audio(self):
        p = pyaudio.PyAudio()

        # Open wave file for output
        with wave.open(OUTPUT_FILE, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            while self.is_processing or not audio_queue.empty():
                if not audio_queue.empty():
                    audio_chunk = audio_queue.get()

                    # Process the audio chunk with SoX (e.g., reducing gain)
                    process = subprocess.Popen(
                        ["sox", "-t", "raw", "-b", "16", "-e", "signed-integer", "-r", str(RATE), "-c", str(CHANNELS), "-",
                         "-t", "raw", "-", "gain", "-3"],  # Example effect: reduce gain by 3 dB
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE
                    )

                    processed_audio, _ = process.communicate(audio_chunk)

                    # Write the processed audio to the wave file
                    wf.writeframes(processed_audio)

        print(f"[Audio] Audio saved to {OUTPUT_FILE}")

    def save_wave(self):        
        with wave.open(OUTPUT_FILE, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            # Retrieve all data from the queue and save it
            while not self.frames.empty():
                wf.writeframes(self.frames.get())

        print(f"[Audio Record Service]:[Saved Audio Record] ", os.path.basename(OUTPUT_FILE))

# Tkinter GUI
class AudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder with SoX")

        # Create the AudioRecorder instance
        self.recorder = AudioRecorder()

        # Start Button
        self.start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=20)

        # Stop Button
        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=20)

    def start_recording(self):
        self.recorder.start_recording()

    def stop_recording(self):
        self.recorder.stop_recording()

# Create Tkinter window and start the app
root = tk.Tk()
app = AudioApp(root)
root.mainloop()
