import os
import queue
import subprocess
import tkinter as tk
import pyaudio
import wave
import threading

class AudioRecorder:
    def __init__(self):        
        self.output_audio_path ="Audio_With_Sox.wav"
        self.channels = 1
        self.rate = 48000  # Lower sample rate for Raspberry Pi
        self.chunk = 1024  # Reduced chunk size for quicker processing
        self.format = pyaudio.paInt16

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
                self.stream = self.audio.open(format=self.format,
                                              channels=self.channels,
                                              rate=self.rate,
                                              input=True,
                                              frames_per_buffer=self.chunk,
                                              input_device_index=1)
              
                print("[Audio Record Service]:[Start Audio Record]")

                while self.recording:
                    try:
                        data = self.stream.read(self.chunk, exception_on_overflow=False)                      
                        self.frames.put(data)  # Add data to the queue
                    except IOError as e:
                        print("Input overflowed:", e)
                        continue

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
        
    def process_audio(self):
        p = pyaudio.PyAudio()

        # Open wave file for output
        with wave.open(self.output_audio_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(self.format))
            wf.setframerate(self.rate)

            while self.is_processing or not self.frames.empty():
                if not self.frames.empty():
                    audio_chunk = self.frames.get()

                    # Process the audio chunk with SoX (e.g., reducing gain)
                    process = subprocess.Popen(
                        ["sox", "-t", "raw", "-b", "16", "-e", "signed-integer", "-r", str(self.rate), "-c", str(self.channels), "-",
                         "-t", "raw", "-", "gain", "-3"],  # Example effect: reduce gain by 3 dB
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE
                    )

                    processed_audio, _ = process.communicate(audio_chunk)

                    # Write the processed audio to the wave file
                    wf.writeframes(processed_audio)

        print(f"[Audio] Audio saved to {self.output_audio_path}")

    def save_wave(self):        
        with wave.open(self.output_audio_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            # Retrieve all data from the queue and save it
            while not self.frames.empty():
                wf.writeframes(self.frames.get())

        print(f"[Audio Record Service]:[Saved Audio Record] ", os.path.basename(self.output_audio_path))


class RecorderApp:
    def __init__(self, root):
        self.root = root
        self.recorder = AudioRecorder()

        # GUI setup
        self.root.title("Audio Recorder")
        self.root.geometry("300x150")

        self.record_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def start_recording(self):
        self.recorder.start_recording()
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.recorder.stop_recording()
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

# Run the Tkinter application
root = tk.Tk()
app = RecorderApp(root)
root.mainloop()