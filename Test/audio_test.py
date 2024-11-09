from datetime import datetime
import os
import queue
import tkinter as tk
import pyaudio
import wave
import threading

class AudioRecorder:
    def __init__(self, record_user_obj):
        self.record_user_obj = record_user_obj
        self.output_audio_path = os.path.join(f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.wav")
        self.channels = 1
        self.rate = 48000  # Lower sample rate for Raspberry Pi
        self.chunk = 1024  # Reduced chunk size for quicker processing
        self.format = pyaudio.paInt16

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.output_stream = None
        self.frames = queue.Queue()  # Use a queue to buffer audio data
        self.recording = False
        self.record_thread = None

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

                self.output_stream = self.audio.open(format=self.format,
                                                     channels=self.channels,
                                                     rate=self.rate,
                                                     frames_per_buffer=self.chunk,
                                                     output=True)

                print("[Start Audio Record]")

                while self.recording:
                    try:
                        data = self.stream.read(self.chunk, exception_on_overflow=False)
                        self.output_stream.write(data)                    
                        self.frames.put(data)  # Add data to the queue
                    except IOError as e:
                        print("Input overflowed:", e)
                        continue

            finally:
                if self.stream is not None:
                    self.stream.stop_stream()
                    self.stream.close()
                if self.output_stream is not None:
                    self.output_stream.stop_stream()
                    self.output_stream.close()
               # Save audio file 
                self.save_wave()

        self.record_thread = threading.Thread(target=record)
        self.record_thread.start()

    def stop_recording(self):
        self.recording = False
        if self.record_thread is not None:
            self.record_thread.join()

    def save_wave(self):      
        with wave.open(self.output_audio_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)           
            while not self.frames.empty():
                wf.writeframes(self.frames.get())

        print(f"[Saved Audio Record] ", os.path.basename(self.output_audio_path))   

    def terminate(self):
        self.audio.terminate()
              
class RecorderApp:
    def __init__(self, root):
        self.root = root
        self.recorder = AudioRecorder()

        # Set up the GUI
        self.root.title("Audio Recorder")
        self.root.geometry("300x150")

        self.record_button = tk.Button(root, text="Record", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def start_recording(self):
        self.recorder.start_recording()
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.recorder.stop_recording() 
        self.recorder.terminate()      
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

# Run the application
root = tk.Tk()
app = RecorderApp(root)
root.mainloop()


