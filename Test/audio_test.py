import tkinter as tk
import pyaudio
import wave
import threading
import scipy.signal
import numpy as np

# Audio recording configuration
CHUNK = 1024  # Frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 16000  # Sample rate (Hz)
OUTPUT_FILE = "output.wav"  # Output file name

class AudioRecorder:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        # Start a new audio stream
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  input_device_index=1,
                                  frames_per_buffer=CHUNK)
        self.frames = []
        self.is_recording = True

        # Start recording in a separate thread
        threading.Thread(target=self.record).start()

    def record(self):
        while self.is_recording:
            try:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                self.frames.append(data)
            except OSError as e:
                print(f"Error: {e}")
                break

    def stop_recording(self):
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

        # Save the recorded frames to a .wav file
        self.save_recording()

    def save_recording(self):
        # Concatenate frames into a single bytes object
        audio_data = np.frombuffer(b''.join(self.frames), dtype=np.int16)
        
        # Apply high-pass filter
        filtered_audio_data = self.high_pass_filter(audio_data)

        # Save filtered audio to a .wav file
        wf = wave.open(OUTPUT_FILE, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        
        # Convert the filtered data back to bytes and write to file
        wf.writeframes(filtered_audio_data.astype(np.int16).tobytes())
        wf.close()
        print("Recording saved as", OUTPUT_FILE)
        
    def high_pass_filter(self, data, cutoff=50, fs=44100, order=5):
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = scipy.signal.butter(order, normal_cutoff, btype='high', analog=False)
        return scipy.signal.filtfilt(b, a, data)
        

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