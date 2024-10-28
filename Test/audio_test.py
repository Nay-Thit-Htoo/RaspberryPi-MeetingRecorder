import tkinter as tk
from tkinter import messagebox
import pyaudio
import wave

class AudioRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")
        
        self.recording = False
        self.frames = []
        
        self.start_button = tk.Button(root, text="Start", command=self.start_recording)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.fs = 44100

        self.p = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        if self.recording:
            return  # Avoid starting multiple recordings
        
        self.frames = []
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.close_stream()
        
        try:
            self.p = pyaudio.PyAudio()  # Reinitialize PyAudio
            self.stream = self.p.open(format=self.sample_format,
                                    channels=self.channels,
                                    rate=self.fs,
                                    frames_per_buffer=self.chunk,
                                    input_device_index=1,
                                    input=True)
            self.record()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open audio stream: {e}")
            self.stop_recording()

    def record(self):
        if self.recording:
            try:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
                self.root.after(100, self.record)
            except IOError as e:
                messagebox.showerror("Error", f"Error reading audio data: {e}")
                self.stop_recording()
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {e}")
                self.stop_recording()

    def stop_recording(self):
        if not self.recording:
            return  # Avoid stopping if not recording
        
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        self.close_stream()
        
        if self.frames:
            try:
                wf = wave.open("output.wav", 'wb')
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.p.get_sample_size(self.sample_format))
                wf.setframerate(self.fs)
                wf.writeframes(b''.join(self.frames))
                wf.close()
                messagebox.showinfo("Recording", "Recording saved as 'output.wav'")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving the recording: {e}")

    def close_stream(self):
        if self.stream is not None:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except IOError as e:
                messagebox.showerror("Error", f"Error stopping audio stream: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {e}")
            finally:
                self.stream = None
        
        if self.p is not None:
            self.p.terminate()
            self.p = None

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorder(root)
    root.mainloop()
