from datetime import datetime
import os
import subprocess
import threading
import wave
import queue
import pyaudio
import file_upload_service

class AudioRecorder:
    def __init__(self, record_user_obj):
        self.record_user_obj = record_user_obj
        self.output_audio_path = os.path.join(
            record_user_obj['usercode'],
            f"{record_user_obj['usercode']}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.wav"
        )
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
                        if self.record_user_obj['is_free_discuss'] == "false":
                            self.frames.put(data)  # Add data to the queue
                    except IOError as e:
                        print("Input overflowed:", e)
                        continue

            finally:
                if self.stream is not None:
                    self.stream.stop_stream()
                    self.stream.close()   
                if self.record_user_obj['is_free_discuss'] == "false":
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

            while self.is_processing or not self.audio_queue.empty():
                if not self.audio_queue.empty():
                    audio_chunk = self.audio_queue.get()

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
        self.create_folder_record_user()
        with wave.open(self.output_audio_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            # Retrieve all data from the queue and save it
            while not self.frames.empty():
                wf.writeframes(self.frames.get())

        print(f"[Audio Record Service]:[Saved Audio Record] ", os.path.basename(self.output_audio_path))

    def create_folder_record_user(self):
        user_code = self.record_user_obj['usercode']
        os.makedirs(user_code, exist_ok=True)

    def terminate(self):
        self.audio.terminate()
        if os.path.exists(self.output_audio_path) and self.record_user_obj['is_free_discuss'] == "false":
            file_upload_service.file_upload_to_server(self.record_user_obj['usercode'], self.record_user_obj)
            file_upload_service.delete_file_after_upload(self.output_audio_path)
            file_upload_service.delete_file_after_upload(self.record_user_obj['usercode'])